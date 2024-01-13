# from config.charger_vehicle_config_bridge import VehicleBridge as Vehicle
# from config.charger_vehicle_config_bridge import ChargerBridge as Charger
# from config.logging_system.logging_config import Logger
# import json
# import requests
# import asyncio

# logger = Logger.logger
# logger_charge_session = logger

# class VehicleSpecyfication:
#     def __init__(self) -> None:
#         self.percent_to_charge = self.percent_required_to_charge(percent=percent)
#         self.kw_needed_to_charge_charge = self.kw_required_to_charge()

#     def percent_required_to_charge(self, percent):
#         percent_needed = percent - self.actual_battery_level
#         return percent_needed
    
#     def kw_required_to_charge(self):
#         kwh_needed = self.percent_to_charge / 100 * self.max_battery_capacity_in_kwh
#         return kwh_needed

# class AcVehicleSpecification:

