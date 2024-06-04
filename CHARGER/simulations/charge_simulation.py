import json

import requests
from config.logging_system.logging_config import ACChargeSessionLogger

logger_server = ACChargeSessionLogger.ac_charge_flow_logger


class ChargeSimulation:
    def percent_required_to_charge(self, percent):
        percent_needed = percent - self.actual_battery_level
        return percent_needed

    def kw_required_to_charge(self):
        kwh_needed = self.percent_to_charge / 100 * self.max_battery_capacity_in_kwh
        return kwh_needed

    def custom_kw_required(self):
        return self.actual_battery_status_in_kwh + self.kw_needed_to_charge_charge

    async def send_kw_per_minute(self, outlet_used, kw_per_min):
        url = f"http://127.0.0.1:5001/vehicle_{str.lower(outlet_used)}/kw_min"
        payload = {"key": kw_per_min}
        headers = {"Content-Type": "application/json"}
        response = requests.patch(url, headers=headers, data=json.dumps(payload))
        return response
