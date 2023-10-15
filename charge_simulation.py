from configs.charger_vehicle_config_bridge import VehicleBridge as Vehicle
from configs.charger_vehicle_config_bridge import ChargerBridge as Charger
import time


class ChargeSimulation:
	def __init__(self):
		# VEHICLE INIT
		self.max_battery_capacity_in_kwh = Vehicle.settings["MAX_BATTERY_CAPACITY_IN_KWH"]
		self.actual_battery_level = Vehicle.settings["BATTERY_LEVEL"]
		self.actual_battery_status_in_kwh = self.current_battery_status_kwh()
		self.kw_needed_to_full_charge = self.energy_needed_to_full_charge()

		# CHARGER INIT
		self.max_charging_power = self.check_connectivity_and_set_max_power()
		self.estimated_time_to_full_charge_in_min = self.estimated_time_needed_to_full_charge()
		self.actual_kw_per_min = self.charged_kw_per_minute()

	def check_connectivity_and_set_max_power(self):
		if Vehicle.settings['CHARGING_PORT'] in Charger.settings['CHARGING_OUTLETS']:
			return Charger.settings[f"MAX_CHARGING_POWER_{Vehicle.settings['CHARGING_PORT']}"]
		else:
			print("CHECK CONNECTIVITY AND TRY AGAIN!")
			return 0

	def current_battery_status_kwh(self):
		actual_battery_status_in_kwh = (self.actual_battery_level / 100) * self.max_battery_capacity_in_kwh
		return actual_battery_status_in_kwh

	def energy_needed_to_full_charge(self):
		kwh_before_losses = self.max_battery_capacity_in_kwh - self.actual_battery_status_in_kwh
		lost_kwh_when_charging = kwh_before_losses * 0.1
		return kwh_before_losses + lost_kwh_when_charging

	def estimated_time_needed_to_full_charge(self):
		time_needed = (self.kw_needed_to_full_charge / self.max_charging_power)
		time_needed_str = str(time_needed).split('.')
		print(time_needed_str)
		hours = time_needed_str[0]
		minutes = time_needed_str[1]
		print(f"Estimated charging time to 80% is {hours} hours and {minutes} minutes")
		return time_needed * 60

	def charged_kw_per_minute(self, charging_after_voltage_drop=None):
		if type(charging_after_voltage_drop) is int or type(charging_after_voltage_drop) is float:
			print("above 80%")
			kw_per_minute = self.actual_kw_per_min / charging_after_voltage_drop
			Charger.settings['ACTUAL_KW_PER_MIN'] = kw_per_minute
			return kw_per_minute
		else:
			print("default")
			kw_per_minute = self.kw_needed_to_full_charge / self.estimated_time_to_full_charge_in_min
			Charger.settings['ACTUAL_KW_PER_MIN'] = kw_per_minute
			return kw_per_minute

	def exchange_kw_to_percent(self):
		actual_percent = round((self.actual_battery_status_in_kwh / self.max_battery_capacity_in_kwh) * 100, 2)
		Vehicle.settings["BATTERY_LEVEL"] = actual_percent
		return actual_percent

	def charging_to_max_battery_capacity(self):
		while self.actual_battery_level < 100:
			print(
				f"DATA PRINTED ONLY FOR TEST'S!!! \n"
				f"actual battery status: {self.actual_battery_status_in_kwh} \n"
				f"actual kw/min{self.actual_kw_per_min} \n"
				f"_____________________________________________________________"
			)
			if Vehicle.connect["is_connected"]:
				if self.actual_battery_status_in_kwh + self.actual_kw_per_min > self.max_battery_capacity_in_kwh:
					self.actual_kw_per_min = self.max_battery_capacity_in_kwh - self.actual_battery_status_in_kwh
					Charger.settings['ACTUAL_KW_PER_MIN'] = self.actual_kw_per_min
				self.actual_battery_status_in_kwh += self.actual_kw_per_min
				self.actual_kw_per_min = self.charged_kw_per_minute(Charger.settings['VOLTAGE_DROP'])
				self.actual_battery_level = self.exchange_kw_to_percent()
				print(f"CHARGING ONGOING: {self.actual_battery_level}%")
				time.sleep(1)
			else:
				return {
					'complete': True,
					'error':
						f"Vehicle disconnected from CHARGER! \n"
						f" Last battery status: {self.actual_battery_level}"
				}
		return {'complete': True, 'error': None}

	def first_stage_charging(self):
		print(self.actual_battery_status_in_kwh)
		while self.actual_battery_level < 80:
			if Vehicle.connect["is_connected"]:
				self.actual_battery_status_in_kwh += self.actual_kw_per_min
				self.actual_battery_level = self.exchange_kw_to_percent()
				print(f"CHARGING ONGOING: {self.actual_battery_level}%")
				time.sleep(1)
			else:
				return {'complete': True, 'error': f"Vehicle disconnected from CHARGER! \n"
												   f" Last battery status: {self.actual_battery_level}"}
		return self.charging_to_max_battery_capacity()

	def prepare_charging(self):
		print(self.first_stage_charging())

# def charging_service(self):
# 	charging_target = self.charging_without_voltage_drop()
# 	# if charging_target["complete"] and charging_target['error'] is None:
# 	# 	charging_target = charging_to_max_battery_capacity(current_battery, kw_per_minute)
# 	return charging_target
#
#
# def prepare_charging(self):
# 	print(type(Charger.settings['ACTUAL_KW_PER_MIN']))
# 	current_battery = self.current_battery_status_kwh()
# 	kwh_to_full_charge = self.energy_needed_to_full_charge()
# 	time_in_hours_to_full_charge = self.estimated_time_needed_to_full_charge()
# 	kw_per_minute = self.charged_kw_per_minute()
# 	print(self.charging_service())

# ___________________________________________________
# def current_battery_status_kwh():
# 	current_battery = (Vehicle.settings["BATTERY_LEVEL"] / 100) * Vehicle.settings["MAX_BATTERY_CAPACITY_IN_KWH"]
# 	Vehicle.settings['ACTUAL_BATTERY_STATUS_IN_KWH'] = current_battery
# 	return current_battery
#
#
# def energy_needed_to_full_charge():
# 	kwh_before_losses = Vehicle.settings["MAX_BATTERY_CAPACITY_IN_KWH"] - Vehicle.settings['ACTUAL_BATTERY_STATUS_IN_KWH']
# 	lost_kwh_when_charging = kwh_before_losses * 0.1
# 	return kwh_before_losses + lost_kwh_when_charging
#
#
# def time_needed_to_full_charge(kwh_to_full_charge):
# 	time_needed = (kwh_to_full_charge / Charger.settings["MAX_CHARGING_POWER"])
# 	time_needed_str = str(time_needed).split('.')
# 	print(time_needed_str)
# 	hours = time_needed_str[0]
# 	minutes = time_needed_str[1]
# 	print(f"Estimated charging time to 80% is {hours} hours and {minutes} minutes")
# 	return time_needed * 60
#
#
# def charged_kw_per_minute(kwh_to_full_charge, time_in_hours_to_full_charge):
# 	kw_per_minute = kwh_to_full_charge / time_in_hours_to_full_charge
# 	Charger.settings['ACTUAL_KW_PER_MIN'] = kw_per_minute
# 	return kw_per_minute
#
#
# def exchange_kw_to_percent():
# 	actual_percent = round((Vehicle.settings['ACTUAL_BATTERY_STATUS_IN_KWH'] / Vehicle.settings["MAX_BATTERY_CAPACITY_IN_KWH"]) * 100, 2)
# 	Vehicle.settings["BATTERY_LEVEL"] = actual_percent
#
#
# def charging_to_max_battery_capacity():
# 	while Vehicle.settings["BATTERY_LEVEL"] < 100:
# 		if Vehicle.connect["is_connected"]:
# 			if Vehicle.settings['ACTUAL_BATTERY_STATUS_IN_KWH'] + Charger.settings['ACTUAL_KW_PER_MIN'] > Vehicle.settings["MAX_BATTERY_CAPACITY_IN_KWH"]:
# 				Charger.settings['ACTUAL_KW_PER_MIN'] = Vehicle.settings["MAX_BATTERY_CAPACITY_IN_KWH"] - Vehicle.settings['ACTUAL_BATTERY_STATUS_IN_KWH']
# 			Vehicle.settings['ACTUAL_BATTERY_STATUS_IN_KWH'] += Charger.settings['ACTUAL_KW_PER_MIN']
# 			Charger.settings['ACTUAL_KW_PER_MIN'] = Charger.settings['ACTUAL_KW_PER_MIN'] / 1.04
# 			exchange_kw_to_percent()
# 			print(f"CHARGING ONGOING: {Vehicle.settings['BATTERY_LEVEL']}%")
# 			time.sleep(1)
# 		else:
#
# 			return {'complete': True, 'error': f"Vehicle disconnected from CHARGER! \n"
# 											   f" Last battery status: {Vehicle.settings['BATTERY_LEVEL']}"}
# 	return {'complete': True, 'error': None}
#
#
# def charging_without_voltage_drop():
# 	print(Vehicle.settings['ACTUAL_BATTERY_STATUS_IN_KWH'])
# 	while Vehicle.settings["BATTERY_LEVEL"] < 80:
# 		if Vehicle.connect["is_connected"]:
# 			Vehicle.settings['ACTUAL_BATTERY_STATUS_IN_KWH'] += Charger.settings['ACTUAL_KW_PER_MIN']
# 			exchange_kw_to_percent()
# 			print(f"CHARGING ONGOING: {Vehicle.settings['BATTERY_LEVEL']}%")
# 			time.sleep(1)
# 		else:
# 			return {'complete': True, 'error': f"Vehicle disconnected from CHARGER! \n"
# 											   f" Last battery status: {Vehicle.settings['BATTERY_LEVEL']}"}
# 	return charging_to_max_battery_capacity()
#
#
# def charging_service():
# 	charging_target = charging_without_voltage_drop()
# 	# if charging_target["complete"] and charging_target['error'] is None:
# 	# 	charging_target = charging_to_max_battery_capacity(current_battery, kw_per_minute)
# 	return charging_target
#
#
# def prepare_charging():
# 	print(type(Charger.settings['ACTUAL_KW_PER_MIN']))
# 	current_battery = current_battery_status_kwh()
# 	kwh_to_full_charge = energy_needed_to_full_charge()
# 	time_in_hours_to_full_charge = time_needed_to_full_charge(kwh_to_full_charge)
# 	kw_per_minute = charged_kw_per_minute(kwh_to_full_charge, time_in_hours_to_full_charge)
# 	print(charging_service())
