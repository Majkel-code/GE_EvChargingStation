from veh_config.vehicle_config_bridge import VehicleBridge as Vehicle
from veh_modules.battery.session_saver import SessionSaver


class AcVehicleSpecification:
    def __init__(self):
        self.actual_kw_per_min = None
        self.max_battery_capacity_in_kwh = Vehicle.settings_ac["MAX_BATTERY_CAPACITY_IN_KWH"]
        self.actual_battery_level = Vehicle.settings_ac["BATTERY_LEVEL"]
        self.actual_battery_status_in_kwh = self.current_battery_status_kwh()
        self.charged_kw = 0

    def exchange_kw_to_percent(self):
        actual_percent = round(
            (self.actual_battery_status_in_kwh / self.max_battery_capacity_in_kwh) * 100,
            2,
        )
        return actual_percent

    def current_battery_status_kwh(self):
        actual_battery_status_in_kwh = (
            self.actual_battery_level / 100
        ) * self.max_battery_capacity_in_kwh
        Vehicle.settings_ac["ACTUAL_BATTERY_STATUS_IN_KWH"] = round(actual_battery_status_in_kwh, 2)
        return actual_battery_status_in_kwh

    def calculate_battery_increase(self):
        self.charged_kw += self.actual_kw_per_min
        self.actual_battery_status_in_kwh += self.actual_kw_per_min
        Vehicle.settings_ac["ACTUAL_BATTERY_STATUS_IN_KWH"] = self.actual_battery_status_in_kwh
        self.actual_battery_level = self.exchange_kw_to_percent()
        Vehicle.settings_ac["BATTERY_LEVEL"] = self.actual_battery_level
        if self.actual_battery_level == 100:
            self.actual_battery_status_in_kwh = self.current_battery_status_kwh()

    def perform_charge_saver(self):
        self.session_id = Vehicle.settings_ac["SESSION_ID"]
        session_saver = SessionSaver()
        session_saver.save_session(
            outlet="AC",
            session_id=self.session_id,
            battery=self.actual_battery_level,
            charged_kw=self.charged_kw,
            time=0,
        )
