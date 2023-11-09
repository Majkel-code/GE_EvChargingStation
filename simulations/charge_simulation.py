from config.charger_vehicle_config_bridge import VehicleBridge as Vehicle
from config.charger_vehicle_config_bridge import ChargerBridge as Charger
from fastapi import Request
import time
from config.logging_system.logging_config import Logger, LoggerChargingSession
import config.cheaker as cheaker

logger = Logger.logger
logger_charge_session = LoggerChargingSession.logger

class ChargeSimulation:
	def __init__(self):
		# VEHICLE INIT
		self.max_battery_capacity_in_kwh = Vehicle.settings["MAX_BATTERY_CAPACITY_IN_KWH"]
		self.actual_battery_level = Vehicle.settings["BATTERY_LEVEL"]
		self.actual_battery_status_in_kwh = self.current_battery_status_kwh()
		self.kw_needed_to_full_charge = self.energy_needed_to_full_charge()
		logger.info("VEHICLE SETTING READ PROPERLY...")

		# CHARGER INIT
		self.max_charging_power = self.check_connectivity_and_set_max_power()
		self.estimated_time_to_full_charge_in_min = self.estimated_time_needed_to_full_charge()
		self.actual_kw_per_min = self.charged_kw_per_minute()
		logger.info("CHARGER SETTINGS READ PROPERLY...")


	def check_connectivity_and_set_max_power(self):
		if Vehicle.settings['CHARGING_PORT'] in Charger.settings['CHARGING_OUTLETS']:
			logger.info("CHECKING CONNECTIVITY...")
			time.sleep(2)
			return Charger.settings[f"MAX_CHARGING_POWER_{Vehicle.settings['CHARGING_PORT']}"]
		else:
			logger.warning("CHECK CONNECTIVITY AND TRY AGAIN!")
			return 0

	def current_battery_status_kwh(self):
		actual_battery_status_in_kwh = (self.actual_battery_level / 100) * self.max_battery_capacity_in_kwh
		return actual_battery_status_in_kwh

	def energy_needed_to_full_charge(self):
		kwh_before_losses = self.max_battery_capacity_in_kwh - self.actual_battery_status_in_kwh
		lost_kwh_when_charging = kwh_before_losses * 0.1
		return kwh_before_losses + lost_kwh_when_charging

	def estimated_time_needed_to_full_charge(self):
		time_needed = round((self.kw_needed_to_full_charge / self.max_charging_power), 2)
		time_needed_str = str(time_needed).split('.')
		hours = time_needed_str[0]
		if len(time_needed_str[1]) < 2:
			minutes = int(time_needed_str[1]) * 10
		else:
			minutes = int(time_needed_str[1])
		logger_charge_session.info(f"Estimated charging time to 80% is {hours} hours and {round((minutes / 100) * 60)} minutes")
		return time_needed * 60

	def charged_kw_per_minute(self, charging_after_voltage_drop=None):
		if type(charging_after_voltage_drop) is int or type(charging_after_voltage_drop) is float:
			kw_per_minute = self.actual_kw_per_min / charging_after_voltage_drop
			Charger.settings['ACTUAL_KW_PER_MIN'] = kw_per_minute
			return kw_per_minute
		else:
			kw_per_minute = self.kw_needed_to_full_charge / self.estimated_time_to_full_charge_in_min
			Charger.settings['ACTUAL_KW_PER_MIN'] = kw_per_minute
			return kw_per_minute

	def exchange_kw_to_percent(self):
		actual_percent = round((self.actual_battery_status_in_kwh / self.max_battery_capacity_in_kwh) * 100, 2)
		Vehicle.settings["BATTERY_LEVEL"] = actual_percent
		return actual_percent

	def charging_to_max_battery_capacity(self):
		while self.actual_battery_level < 100 and cheaker.check_server_is_alive():
			logger_charge_session.debug("INFORMATION ABOUT ACTUAL CHARGING STATE.... ")
			logger_charge_session.debug(f"actual battery status: {self.actual_battery_status_in_kwh} ")
			logger_charge_session.debug(f"actual kw/min{self.actual_kw_per_min}")
			logger_charge_session.debug("_____________________________________________________________")
			if Vehicle.connect["is_connected"]: 
				if self.actual_battery_status_in_kwh + self.actual_kw_per_min > self.max_battery_capacity_in_kwh:
					self.actual_kw_per_min = self.max_battery_capacity_in_kwh - self.actual_battery_status_in_kwh
					Charger.settings['ACTUAL_KW_PER_MIN'] = self.actual_kw_per_min
				self.actual_battery_status_in_kwh += self.actual_kw_per_min
				self.actual_kw_per_min = self.charged_kw_per_minute(Charger.settings['VOLTAGE_DROP'])
				self.actual_battery_level = self.exchange_kw_to_percent()
				logger_charge_session.info(f"CHARGING ONGOING: {self.actual_battery_level}%")
				time.sleep(1)
			else:
				logger_charge_session.warning("VEHICLE DISCONNECTED CHARGE SESSION ABORD!")
				Request.get("http://127.0.0.1:5000/vehicle/disconnect")
				return {
					'complete': True,
					'error':
						f"Vehicle disconnected from CHARGER! \n"
						f" Last battery status: {self.actual_battery_level}"
				}
		logger_charge_session.info("CHARGE SESSION COMPLETE...")
		return {'complete': True, 'error': None}

	def first_stage_charging(self):
		while self.actual_battery_level < 80:
			if Vehicle.connect["is_connected"] and cheaker.check_server_is_alive():
				self.actual_battery_status_in_kwh += self.actual_kw_per_min
				self.actual_battery_level = self.exchange_kw_to_percent()
				logger_charge_session.info(f"CHARGING ONGOING: {self.actual_battery_level}%")
				time.sleep(1)
			else:
				logger_charge_session.warning("VEHICLE DISCONNECTED CHARGE SESSION ABORD!")
				return {'complete': True, 'error': f"Vehicle disconnected from CHARGER! \n"
												   f" Last battery status: {self.actual_battery_level}"}
		logger_charge_session.info("80% OF BATTERY LEVEL ACHIVE...")
		return self.charging_to_max_battery_capacity()

	def prepare_charging(self):
		logger_charge_session.info("STARTING CHARGING SESSION...")
		print(self.first_stage_charging())
