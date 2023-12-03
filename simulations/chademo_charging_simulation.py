from simulations.charge_simulation import ChargeSimulation
from config.charger_vehicle_config_bridge import VehicleBridge as Vehicle
from config.charger_vehicle_config_bridge import ChargerBridge as Charger
from fastapi import Request
import time
from config.logging_system.logging_config import Logger
import config.cheaker as cheaker

logger = Logger.logger
logger_charge_session = logger


class ChademoVehicle(ChargeSimulation):
    def __init__(self):
        super().__init__()
        # VEHICLE INIT
        self.max_battery_capacity_in_kwh = Vehicle.settings_chademo["MAX_BATTERY_CAPACITY_IN_KWH"]
        self.actual_battery_level = Vehicle.settings_chademo["BATTERY_LEVEL"]
        self.actual_battery_status_in_kwh = self.current_battery_status_kwh()
        self.percent_to_charge = None
        self.kw_needed_to_charge_charge = None
        logger.info("VEHICLE SETTING READ PROPERLY...")
        # CHARGER INIT
        self.max_charging_power = self.check_connectivity_and_set_max_power()

    def check_connectivity_and_set_max_power(self):
        if Vehicle.settings_chademo["CHARGING_PORT"] in Charger.settings["CHARGING_OUTLETS"]:
            logger.info("CHECKING CONNECTIVITY...")
            time.sleep(2)
            return Charger.settings[f"MAX_CHARGING_POWER_{Vehicle.settings_chademo['CHARGING_PORT']}"]
        else:
            logger.warning("CHECK CONNECTIVITY AND TRY AGAIN!")
            return 0

    def current_battery_status_kwh(self):
        actual_battery_status_in_kwh = (self.actual_battery_level / 100) * self.max_battery_capacity_in_kwh
        Vehicle.settings_chademo["ACTUAL_BATTERY_STATUS_IN_KWH"] = round(actual_battery_status_in_kwh, 2)
        return actual_battery_status_in_kwh

    def charging_to_max_battery_capacity(self, percent):
        Charger._charging_finished_ = False
        while (
            self.actual_battery_level < 100 and cheaker.check_server_is_alive() and self.actual_battery_level <= percent
        ):
            logger_charge_session.debug("INFORMATION ABOUT ACTUAL CHADEMO CHARGING STATE.... ")
            logger_charge_session.debug(f"chademo actual battery status: {self.actual_battery_status_in_kwh}")
            logger_charge_session.debug(f"chademo actual kw/min: {self.actual_kw_per_min}")
            logger_charge_session.debug("_____________________________________________________________")
            if Vehicle._connected_chademo_:
                if self.actual_battery_status_in_kwh + self.actual_kw_per_min > self.max_battery_capacity_in_kwh:
                    self.actual_kw_per_min = self.max_battery_capacity_in_kwh - self.actual_battery_status_in_kwh
                    Charger.settings["ACTUAL_KW_PER_MIN"] = self.actual_kw_per_min
                self.actual_battery_status_in_kwh += self.actual_kw_per_min
                self.actual_kw_per_min = self.charged_kw_per_minute(Charger.settings["VOLTAGE_DROP"])
                self.actual_battery_level = self.exchange_kw_to_percent()
                self.actual_battery_status_in_kwh = self.current_battery_status_kwh()
                logger_charge_session.info(f"CHADEMO CHARGING ONGOING: {self.actual_battery_level}%")
                Charger._energy_is_send_loop_chademo_ += 1
                time.sleep(1)
            else:
                logger_charge_session.warning("VEHICLE DISCONNECTED CHADEMO CHARGE SESSION ABORD!")
                Request.get("http://127.0.0.1:5000/vehicle/disconnect")
                return {
                    "complete": True,
                    "error": f"Vehicle disconnected from CHARGER! \n"
                    f" Last battery status: {self.actual_battery_level}",
                }
        logger_charge_session.info(f"{percent}% OF BATTERY LEVEL ACHIVE...")
        return {"complete": True, "error": None}

    def first_stage_charging(self, percent):
        if self.actual_battery_level < self.effective_charging_cap:
            Charger._charging_finished_ = False
            while self.actual_battery_level <= percent:
                if self.actual_battery_level >= self.effective_charging_cap:
                    logger_charge_session.info(f"{self.effective_charging_cap}% OF BATTERY LEVEL ACHIVE...")
                    return {"complete": True, "error": None}
                if Vehicle._connected_chademo_ and cheaker.check_server_is_alive():
                    self.actual_battery_status_in_kwh += self.actual_kw_per_min
                    self.actual_battery_level = self.exchange_kw_to_percent()
                    Vehicle.settings_chademo["BATTERY_LEVEL"] = self.actual_battery_level
                    self.actual_battery_status_in_kwh = self.current_battery_status_kwh()
                    logger_charge_session.info(f"CHADEMO CHARGING ONGOING: {self.actual_battery_level}%")
                    Charger._energy_is_send_loop_chademo_ += 1
                    time.sleep(1)
                else:
                    logger_charge_session.warning("VEHICLE DISCONNECTED CHARGE SESSION ABORD!")
                    return {
                        "complete": True,
                        "error": f"Vehicle disconnected from CHARGER! \n"
                        f" Last battery status: {self.actual_battery_level}",
                    }
            logger_charge_session.info(f"{percent}% OF BATTERY LEVEL ACHIVE...")
            return {"complete": True, "error": None}
        return {"complete": True, "error": None}

    def prepare_chademo_charging(self, percent: int = 100):
        logger_charge_session.info("STARTING CHARGING SESSION...")
        # VEHICLE INIT
        self.percent_to_charge = self.percent_required_to_charge(percent=percent)
        self.kw_needed_to_charge_charge = self.kw_required_to_charge()
        # CHARGER INIT
        self.estimated_time_to_full_charge_in_min = self.estimated_time_needed_to_full_charge(percent=percent)
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
            logger_charge_session.info(f"CHADEMO SESSION END!")
            Charger._energy_is_send_loop_chademo_ = 0
            return charging_with_energy_drop
        logger_charge_session.info(f"CHADEMO SESSION END!")
        logger_charge_session.info(f"PLEASE DISCONNECT YOUR VEHICLE..")
        logger_charge_session.info(f"CHARGER STATE: IDLE")
        Charger._charging_finished_chademo_ = True
        Charger._energy_is_send_loop_chademo_ = 0
        return constant_power_level_charging
