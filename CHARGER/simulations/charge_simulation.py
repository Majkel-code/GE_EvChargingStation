from config.charger_vehicle_config_bridge import VehicleBridge as Vehicle
from config.charger_vehicle_config_bridge import ChargerBridge as Charger
from config.logging_system.logging_config import Logger
import json
import requests
import asyncio

logger = Logger.logger
logger_charge_session = logger


class ChargeSimulation:
    def __init__(self):
        # CHARGER INIT
        self.effective_charging_cap = Charger.settings["EFFECTIVE_CHARGING_CAP"]
        self.estimated_time_to_full_charge_in_min = None
        logger.info("CHARGER SETTINGS READ PROPERLY...")

    def percent_required_to_charge(self, percent):
        percent_needed = percent - self.actual_battery_level
        return percent_needed

    def kw_required_to_charge(self):
        kwh_needed = self.percent_to_charge / 100 * self.max_battery_capacity_in_kwh
        return kwh_needed

    def calculate_displayed_time(self, percent, time_in_minutes):
        time_in_minutes = int(round(time_in_minutes, 0))
        h = time_in_minutes // 60
        m = time_in_minutes % 60
        logger.info(f"Estimated charging time to {percent}% is {h} hours and {m} minutes")

    def estimated_time_needed_to_full_charge(self, percent):
        time_needed = round((self.kw_needed_to_charge_charge / self.max_charging_power), 2)
        self.calculate_displayed_time(percent=percent, time_in_minutes=time_needed * 60)
        return time_needed * 60


    def exchange_kw_to_percent(self):
        actual_percent = round((self.actual_battery_status_in_kwh / self.max_battery_capacity_in_kwh) * 100, 2)
        return actual_percent
    


    async def send_specification_to_vehicle(self, outlet_used):
        url = f"http://127.0.0.1:5001/vehicle_{str.lower(outlet_used)}/spec"
        if outlet_used == "AC":
            payload = Vehicle.settings_ac
        elif outlet_used == "CHADEMO":
            payload = Vehicle.settings_chademo

        headers = {
        'Content-Type': 'application/json'
        }
        print(json.dumps(payload))
        response = requests.patch(url, headers=headers, data=json.dumps(payload))
        if response.ok:
            return True