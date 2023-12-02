from config.charger_vehicle_config_bridge import VehicleBridge as Vehicle
from config.charger_vehicle_config_bridge import ChargerBridge as Charger
from config.logging_system.logging_config import Logger

logger = Logger.logger
logger_charge_session = logger

class ChargeSimulation:
	def __init__(self):
		# CHARGER INIT
		self.effective_charging_cap = Charger.settings['EFFECTIVE_CHARGING_CAP']
		self.estimated_time_to_full_charge_in_min = None
		self.actual_kw_per_min = None
		logger.info("CHARGER SETTINGS READ PROPERLY...")

		
	def percent_required_to_charge(self, percent):
		percent_needed = percent - self.actual_battery_level
		return percent_needed
	
	def kw_required_to_charge(self):
		kwh_needed = self.percent_to_charge / 100 * self.max_battery_capacity_in_kwh
		return kwh_needed

	def calculate_displayed_time(self, percent, time_in_minutes):
		time_in_minutes = int(round(time_in_minutes, 0))
		h=time_in_minutes//60
		m=time_in_minutes%60
		logger.info(f"Estimated charging time to {percent}% is {h} hours and {m} minutes")

	def estimated_time_needed_to_full_charge(self, percent):
		time_needed = round((self.kw_needed_to_charge_charge / self.max_charging_power), 2)
		self.calculate_displayed_time(percent=percent, time_in_minutes=time_needed * 60)
		return time_needed * 60

	def charged_kw_per_minute(self, charging_after_voltage_drop=None):
		if type(charging_after_voltage_drop) is int or type(charging_after_voltage_drop) is float:
			kw_per_minute = self.actual_kw_per_min / charging_after_voltage_drop
			Charger.settings['ACTUAL_KW_PER_MIN'] = kw_per_minute
			return kw_per_minute
		else:
			kw_per_minute = self.kw_needed_to_charge_charge / self.estimated_time_to_full_charge_in_min
			Charger.settings['ACTUAL_KW_PER_MIN'] = kw_per_minute
			return kw_per_minute

	def exchange_kw_to_percent(self):
		actual_percent = round((self.actual_battery_status_in_kwh / self.max_battery_capacity_in_kwh) * 100, 2)
		return actual_percent
