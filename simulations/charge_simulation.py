from config.charger_vehicle_config_bridge import VehicleBridge as Vehicle
from config.charger_vehicle_config_bridge import ChargerBridge as Charger
from fastapi import Request
import time
from config.logging_system.logging_config import Logger
import config.cheaker as cheaker

logger = Logger.logger
logger_charge_session = logger

class ChargeSimulation:
	def __init__(self):
		# VEHICLE INIT
		self.max_battery_capacity_in_kwh = Vehicle.settings["MAX_BATTERY_CAPACITY_IN_KWH"]
		self.actual_battery_level = Vehicle.settings["BATTERY_LEVEL"]
		self.actual_battery_status_in_kwh = self.current_battery_status_kwh()
		self.percent_to_charge = None
		self.kw_needed_to_charge_charge = None
		logger.info("VEHICLE SETTING READ PROPERLY...")

		# CHARGER INIT
		self.max_charging_power = self.check_connectivity_and_set_max_power()
		self.effective_charging_cap = Charger.settings['EFFECTIVE_CHARGING_CAP']
		self.estimated_time_to_full_charge_in_min = None
		self.actual_kw_per_min = None
		logger.info("CHARGER SETTINGS READ PROPERLY...")


	def check_connectivity_and_set_max_power(self):
		if Vehicle.settings['CHARGING_PORT'] in Charger.settings['CHARGING_OUTLETS']:
			logger.info("CHECKING CONNECTIVITY...")
			time.sleep(2)
			return Charger.settings[f"MAX_CHARGING_POWER_{Vehicle.settings['CHARGING_PORT']}"]
		else:
			logger.warning("CHECK CONNECTIVITY AND TRY AGAIN!")
			return 0
		
	def percent_required_to_charge(self, percent):
		percent_needed = percent - self.actual_battery_level
		return percent_needed
	
	def kw_required_to_charge(self):
		kwh_needed = self.percent_to_charge / 100 * self.max_battery_capacity_in_kwh
		return kwh_needed

	def current_battery_status_kwh(self):
		actual_battery_status_in_kwh = (self.actual_battery_level / 100) * self.max_battery_capacity_in_kwh
		Vehicle.settings['ACTUAL_BATTERY_STATUS_IN_KWH'] = round(actual_battery_status_in_kwh, 2)
		return actual_battery_status_in_kwh

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
		Vehicle.settings["BATTERY_LEVEL"] = actual_percent
		return actual_percent

	def charging_to_max_battery_capacity(self, percent):
		Charger._charging_finished_ = False
		while self.actual_battery_level < 100 and cheaker.check_server_is_alive() and self.actual_battery_level <= percent:
			logger_charge_session.debug("INFORMATION ABOUT ACTUAL CHARGING STATE.... ")
			logger_charge_session.debug(f"actual battery status: {self.actual_battery_status_in_kwh}%")
			logger_charge_session.debug(f"actual kw/min: {self.actual_kw_per_min}")
			logger_charge_session.debug("_____________________________________________________________")
			if Vehicle._connected_: 
				if self.actual_battery_status_in_kwh + self.actual_kw_per_min > self.max_battery_capacity_in_kwh:
					self.actual_kw_per_min = self.max_battery_capacity_in_kwh - self.actual_battery_status_in_kwh
					Charger.settings['ACTUAL_KW_PER_MIN'] = self.actual_kw_per_min
				self.actual_battery_status_in_kwh += self.actual_kw_per_min
				self.actual_kw_per_min = self.charged_kw_per_minute(Charger.settings['VOLTAGE_DROP'])
				self.actual_battery_level = self.exchange_kw_to_percent()
				self.actual_battery_status_in_kwh = self.current_battery_status_kwh()
				logger_charge_session.info(f"CHARGING ONGOING: {self.actual_battery_level}%")
				Charger._energy_is_send_loop_ += 1
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
		logger_charge_session.info(f"{percent}% OF BATTERY LEVEL ACHIVE...")
		return {'complete': True, 'error': None}

	def first_stage_charging(self, percent):
		if self.actual_battery_level < self.effective_charging_cap:
			Charger._charging_finished_ = False
			while self.actual_battery_level <= percent:
				if self.actual_battery_level >= self.effective_charging_cap:
					logger_charge_session.info(f"{self.effective_charging_cap}% OF BATTERY LEVEL ACHIVE...")
					return {'complete': True, 'error': None}
				if Vehicle._connected_ and cheaker.check_server_is_alive():
					self.actual_battery_status_in_kwh += self.actual_kw_per_min
					self.actual_battery_level = self.exchange_kw_to_percent()
					self.actual_battery_status_in_kwh = self.current_battery_status_kwh()
					logger_charge_session.info(f"CHARGING ONGOING: {self.actual_battery_level}%")
					Charger._energy_is_send_loop_ += 1
					time.sleep(1)
				else:
					logger_charge_session.warning("VEHICLE DISCONNECTED CHARGE SESSION ABORD!")
					return {'complete': True, 'error': f"Vehicle disconnected from CHARGER! \n"
													f" Last battery status: {self.actual_battery_level}"}
			logger_charge_session.info(f"{percent}% OF BATTERY LEVEL ACHIVE...")
			return {'complete': True, 'error': None}
		return {'complete': True, 'error': None}
		

	def prepare_charging(self, percent: int = 100):
		logger_charge_session.info("STARTING CHARGING SESSION...")
		# VEHICLE INIT
		self.percent_to_charge = self.percent_required_to_charge(percent=percent)
		self.kw_needed_to_charge_charge = self.kw_required_to_charge()
		# CHARGER INIT
		self.estimated_time_to_full_charge_in_min = self.estimated_time_needed_to_full_charge(percent=percent)
		self.actual_kw_per_min = self.charged_kw_per_minute()
		# CHARGE SESSION
		constant_power_level_charging = self.first_stage_charging(percent=percent)
		if constant_power_level_charging['complete'] and constant_power_level_charging['error'] is None and percent > self.effective_charging_cap:
			charging_with_energy_drop = self.charging_to_max_battery_capacity(percent=percent)
			Charger._charging_finished_ = True
			Charger._energy_is_send_loop_ = 0
			return charging_with_energy_drop
		Charger._charging_finished_ = True
		Charger._energy_is_send_loop_ = 0
		return constant_power_level_charging