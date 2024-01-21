import asyncio
import time

from config.charger_vehicle_config_bridge import ChargerBridge as Charger
from config.charger_vehicle_config_bridge import IsServerAlive as Main_server
from config.charger_vehicle_config_bridge import VehicleBridge as Vehicle
from config.logging_system.logging_config import CHADEMOChargeSessionLogger
from simulations.charge_simulation import ChargeSimulation

chademo_logger = CHADEMOChargeSessionLogger.chademo_charge_flow_logger


class ChademoVehicle(ChargeSimulation):
    def __init__(self):
        super().__init__()
        Vehicle.take_chademo_vehicle_specification()
        # CHARGER INIT
        self.max_charging_power = self.check_connectivity_and_set_max_power()
        self.actual_kw_per_min = None
        chademo_logger.info("CHARGER SETTINGS READ PROPERLY...")
        # VEHICLE INIT
        self.effective_charging_cap = Vehicle.settings_chademo["EFFECTIVE_CHARGING_CAP"]
        self.estimated_time_to_full_charge_in_min = None
        self.max_battery_capacity_in_kwh = Vehicle.settings_chademo["MAX_BATTERY_CAPACITY_IN_KWH"]
        self.actual_battery_level = Vehicle.settings_chademo["BATTERY_LEVEL"]
        self.actual_battery_status_in_kwh = Vehicle.settings_chademo["ACTUAL_BATTERY_STATUS_IN_KWH"]
        self.percent_to_charge = None
        self.kw_needed_to_charge_charge = None
        chademo_logger.info("VEHICLE SETTING READ PROPERLY...")

    def check_connectivity_and_set_max_power(self):
        if Vehicle.settings_chademo["CHARGING_PORT"] in Charger.settings["CHARGING_OUTLETS"]:
            chademo_logger.info("CHECKING CONNECTIVITY...")
            time.sleep(2)
            return Charger.settings[
                f"MAX_CHARGING_POWER_{Vehicle.settings_chademo['CHARGING_PORT']}"
            ]
        else:
            chademo_logger.warning("CHECK CONNECTIVITY AND TRY AGAIN!")
            return 0

    def calculate_displayed_time(self, percent, time_in_minutes):
        time_in_minutes = int(round(time_in_minutes, 0))
        h = time_in_minutes // 60
        m = time_in_minutes % 60
        chademo_logger.info(f"Estimated charging time to {percent}% is {h} hours and {m} minutes")

    def estimated_time_needed_to_full_charge(self, percent):
        time_needed = round((self.kw_needed_to_charge_charge / self.max_charging_power), 2)
        self.calculate_displayed_time(percent=percent, time_in_minutes=time_needed * 60)
        return time_needed * 60

    def send_energy(self):
        asyncio.run(self.send_kw_per_minute("CHADEMO", self.actual_kw_per_min))

    def charged_kw_per_minute(self, charging_after_voltage_drop=None):
        if type(charging_after_voltage_drop) is int or type(charging_after_voltage_drop) is float:
            kw_per_minute = self.actual_kw_per_min / charging_after_voltage_drop
            Charger.settings["CHADEMO_ACTUAL_KW_PER_MIN"] = kw_per_minute
            return kw_per_minute
        else:
            kw_per_minute = (
                self.kw_needed_to_charge_charge / self.estimated_time_to_full_charge_in_min
            )
            Charger.settings["CHADEMO_ACTUAL_KW_PER_MIN"] = kw_per_minute
            return kw_per_minute

    def charging_to_max_battery_capacity(self, percent):
        Charger._charging_finished_ = False
        while (
            self.actual_battery_level < 100
            and Main_server.check_server_is_alive()
            and self.actual_battery_level <= percent
        ):
            Vehicle.take_chademo_vehicle_specification()
            self.actual_battery_level = Vehicle.settings_chademo["BATTERY_LEVEL"]
            self.actual_battery_status_in_kwh = Vehicle.settings_chademo[
                "ACTUAL_BATTERY_STATUS_IN_KWH"
            ]
            chademo_logger.debug("INFORMATION ABOUT ACTUAL CHADEMO CHARGING STATE.... ")
            chademo_logger.debug(
                f"chademo actual battery status: {self.actual_battery_status_in_kwh}"
            )
            chademo_logger.debug(f"chademo actual kw/min: {self.actual_kw_per_min}")
            chademo_logger.debug("_____________________________________________________________")
            if Vehicle._connected_chademo_:
                if (
                    self.actual_battery_status_in_kwh + self.actual_kw_per_min
                    > self.max_battery_capacity_in_kwh
                ):
                    print("last tick")
                    self.actual_kw_per_min = (
                        self.max_battery_capacity_in_kwh - self.actual_battery_status_in_kwh
                    )
                    Charger.settings["CHADEMO_ACTUAL_KW_PER_MIN"] = self.actual_kw_per_min
                else:
                    self.actual_kw_per_min = self.charged_kw_per_minute(
                        Charger.settings["VOLTAGE_DROP_CHADEMO"]
                    )
                self.actual_battery_status_in_kwh += self.actual_kw_per_min
                self.send_energy()
                chademo_logger.info(f"CHADEMO CHARGING ONGOING: {self.actual_battery_level}%")
                Charger._energy_is_send_loop_chademo_ += 1
                time.sleep(1)
            else:
                chademo_logger.warning("VEHICLE DISCONNECTED CHADEMO CHARGE SESSION ABORD!")
                return {
                    "complete": True,
                    "error": f"Vehicle disconnected from CHARGER! \n"
                    f" Last battery status: {self.actual_battery_level}",
                }
        chademo_logger.info(f"{percent}% OF BATTERY LEVEL ACHIVE...")
        return {"complete": True, "error": None}

    def first_stage_charging(self, percent):
        if self.actual_battery_level < self.effective_charging_cap:
            Charger._charging_finished_ = False
            while self.actual_battery_level <= percent and Main_server.check_server_is_alive():
                Vehicle.take_chademo_vehicle_specification()
                if self.actual_battery_level >= self.effective_charging_cap:
                    chademo_logger.info(
                        f"{self.effective_charging_cap}% OF BATTERY LEVEL ACHIVE..."
                    )
                    return {"complete": True, "error": None}
                if Vehicle._connected_chademo_:
                    self.actual_battery_level = Vehicle.settings_chademo["BATTERY_LEVEL"]
                    self.actual_battery_status_in_kwh = Vehicle.settings_chademo[
                        "ACTUAL_BATTERY_STATUS_IN_KWH"
                    ]
                    self.actual_battery_status_in_kwh += self.actual_kw_per_min
                    self.send_energy()
                    chademo_logger.info(f"CHADEMO CHARGING ONGOING: {self.actual_battery_level}%")
                    Charger._energy_is_send_loop_chademo_ += 1
                    time.sleep(1)
                else:
                    chademo_logger.warning("VEHICLE DISCONNECTED CHARGE SESSION ABORD!")
                    return {
                        "complete": True,
                        "error": f"Vehicle disconnected from CHARGER! \n"
                        f" Last battery status: {self.actual_battery_level}",
                    }
            chademo_logger.info(f"{percent}% OF BATTERY LEVEL ACHIVE...")
            return {"complete": True, "error": None}
        return {"complete": True, "error": None}

    def prepare_chademo_charging(self, percent: int = 100):
        chademo_logger.info("STARTING CHARGING SESSION...")
        # VEHICLE INIT
        self.percent_to_charge = self.percent_required_to_charge(percent=percent)
        self.kw_needed_to_charge_charge = self.kw_required_to_charge()
        # CHARGER INIT
        self.estimated_time_to_full_charge_in_min = self.estimated_time_needed_to_full_charge(
            percent=percent
        )
        self.actual_kw_per_min = self.charged_kw_per_minute()
        # CHARGE SESSION
        constant_power_level_charging = self.first_stage_charging(percent=percent)
        if (
            constant_power_level_charging["complete"]
            and constant_power_level_charging["error"] is None
            and percent > self.effective_charging_cap
        ):
            charging_with_energy_drop = self.charging_to_max_battery_capacity(percent=percent)
            Charger._charging_finished_chademo_ = True
            chademo_logger.info("CHADEMO SESSION END!")
            Charger._energy_is_send_loop_chademo_ = 0
            return charging_with_energy_drop
        chademo_logger.info("CHADEMO SESSION END!")
        chademo_logger.info("PLEASE DISCONNECT YOUR VEHICLE..")
        chademo_logger.info("CHARGER STATE: IDLE")
        Charger._charging_finished_chademo_ = True
        Charger._energy_is_send_loop_chademo_ = 0
        return constant_power_level_charging
