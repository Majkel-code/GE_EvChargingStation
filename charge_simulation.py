from charger_vehicle_config import VehicleBridge as Vehicle
from charger_vehicle_config import ChargerBridge as Charger
import time


def current_battery_status_kwh():
	current_battery = (Vehicle.settings["BATTERY_LEVEL"] / 100) * Vehicle.settings["MAX_BATTERY_CAPACITY_IN_KWH"]
	Vehicle.settings['ACTUAL_BATTERY_STATUS_IN_KWH'] = current_battery
	return current_battery


def energy_needed_to_full_charge():
	kwh_before_losses = Vehicle.settings["MAX_BATTERY_CAPACITY_IN_KWH"] - Vehicle.settings['ACTUAL_BATTERY_STATUS_IN_KWH']
	lost_kwh_when_charging = kwh_before_losses * 0.1
	return kwh_before_losses + lost_kwh_when_charging


def time_needed_to_full_charge(kwh_to_full_charge):
	time_needed = (kwh_to_full_charge / Charger.settings["MAX_CHARGING_POWER"])
	time_needed_str = str(time_needed).split('.')
	print(time_needed_str)
	hours = time_needed_str[0]
	minutes = time_needed_str[1]
	print(f"Estimated charging time to 80% is {hours} hours and {minutes} minutes")
	return time_needed * 60


def charged_kw_per_minute(kwh_to_full_charge, time_in_hours_to_full_charge):
	kw_per_minute = kwh_to_full_charge / time_in_hours_to_full_charge
	Charger.settings['ACTUAL_KW_PER_MIN'] = kw_per_minute
	return kw_per_minute


def exchange_kw_to_percent():
	actual_percent = round((Vehicle.settings['ACTUAL_BATTERY_STATUS_IN_KWH'] / Vehicle.settings["MAX_BATTERY_CAPACITY_IN_KWH"]) * 100, 2)
	Vehicle.settings["BATTERY_LEVEL"] = actual_percent


def charging_to_max_battery_capacity():
	while Vehicle.settings["BATTERY_LEVEL"] < 100:
		if Vehicle.connect["is_connected"]:
			if Vehicle.settings['ACTUAL_BATTERY_STATUS_IN_KWH'] + Charger.settings['ACTUAL_KW_PER_MIN'] > Vehicle.settings["MAX_BATTERY_CAPACITY_IN_KWH"]:
				Charger.settings['ACTUAL_KW_PER_MIN'] = Vehicle.settings["MAX_BATTERY_CAPACITY_IN_KWH"] - Vehicle.settings['ACTUAL_BATTERY_STATUS_IN_KWH']
			Vehicle.settings['ACTUAL_BATTERY_STATUS_IN_KWH'] += Charger.settings['ACTUAL_KW_PER_MIN']
			Charger.settings['ACTUAL_KW_PER_MIN'] = Charger.settings['ACTUAL_KW_PER_MIN'] / 1.04
			exchange_kw_to_percent()
			print(f"CHARGING ONGOING: {Vehicle.settings['BATTERY_LEVEL']}%")
			time.sleep(1)
		else:

			return {'complete': True, 'error': f"Vehicle disconnected from CHARGER! \n"
											   f" Last battery status: {Vehicle.settings['BATTERY_LEVEL']}"}
	return {'complete': True, 'error': None}


def charging_without_voltage_drop():
	print(Vehicle.settings['ACTUAL_BATTERY_STATUS_IN_KWH'])
	while Vehicle.settings["BATTERY_LEVEL"] < 80:
		if Vehicle.connect["is_connected"]:
			Vehicle.settings['ACTUAL_BATTERY_STATUS_IN_KWH'] += Charger.settings['ACTUAL_KW_PER_MIN']
			exchange_kw_to_percent()
			print(f"CHARGING ONGOING: {Vehicle.settings['BATTERY_LEVEL']}%")
			time.sleep(1)
		else:
			return {'complete': True, 'error': f"Vehicle disconnected from CHARGER! \n"
											   f" Last battery status: {Vehicle.settings['BATTERY_LEVEL']}"}
	return charging_to_max_battery_capacity()


def charging_service():
	charging_target = charging_without_voltage_drop()
	# if charging_target["complete"] and charging_target['error'] is None:
	# 	charging_target = charging_to_max_battery_capacity(current_battery, kw_per_minute)
	return charging_target


def prepare_charging():
	print(type(Charger.settings['ACTUAL_KW_PER_MIN']))
	current_battery = current_battery_status_kwh()
	kwh_to_full_charge = energy_needed_to_full_charge()
	time_in_hours_to_full_charge = time_needed_to_full_charge(kwh_to_full_charge)
	kw_per_minute = charged_kw_per_minute(kwh_to_full_charge, time_in_hours_to_full_charge)
	print(charging_service())


# ________________________________________________

#
# def actual_capacity():
# 	capacity = (Vehicle.settings["BATTERY_LEVEL"] / 100) * Vehicle.settings["MAX_BATTERY_CAPACITY"]
# 	return capacity
#
#
# def target_state_of_charge():
# 	target_percent = 80
# 	actual_percent = Vehicle.settings["BATTERY_LEVEL"]
# 	return target_percent - actual_percent
#
#
# def transfer_percent_to_kwh(lacking_percent):
# 	target_kwh = (lacking_percent / 100) * Vehicle.settings["MAX_BATTERY_CAPACITY"]
# 	return target_kwh
#
#
# def compensate_for_losses(target_kwh_before_losses):
# 	losses_kwh = 10 / 100 * target_kwh_before_losses
# 	return target_kwh_before_losses + losses_kwh
#
#
# def time_needed_to_target(target_kwh):
# 	time_needed = (target_kwh / Charger.settings["MAX_CHARGING_POWER"]) * 60
# 	return time_needed
#
#
# def kw_per_minutes(target_kwh, time_needed_in_minutes):
# 	kw_per_minute = target_kwh / time_needed_in_minutes
# 	return kw_per_minute
#
#
# def transfer_kw_to_percent(actual_battery_state):
# 	actual_percent = round((actual_battery_state / Vehicle.settings["MAX_BATTERY_CAPACITY"]) * 100, 2)
# 	Vehicle.settings["BATTERY_LEVEL"] = actual_percent
#
#
# def simulate_charging_to_target(actual_battery_state, kw_per_minute):
# 	while Vehicle.settings["BATTERY_LEVEL"] < 80:
# 		if Vehicle.connect["is_connected"]:
# 			actual_battery_state += kw_per_minute
# 			transfer_kw_to_percent(actual_battery_state)
# 			time.sleep(0.5)
# 			print(f"CHARGING ONGOING: {Vehicle.settings['BATTERY_LEVEL']}%")
# 		elif not Vehicle.connect["is_connected"]:
# 			return {"complete": True,
# 					"error": f"Charging finished, OUTLET disconnected! \n BATTERY:{Vehicle.settings['BATTERY_LEVEL']}%"}
# 		else:
# 			return {"complete": False, "error": "Unexpected error!"}
# 	return {"complete": True, "error": None}
#
#
# def simulate_charging_to_max_battery_level(actual_battery_state, kw_per_minute):
# 	while Vehicle.settings["BATTERY_LEVEL"] < 100:
# 		if Vehicle.connect["is_connected"]:
# 			actual_battery_state += kw_per_minute / 1.1
# 			transfer_kw_to_percent(actual_battery_state)
# 			time.sleep(0.5)
# 			print(f"CHARGING ONGOING: {Vehicle.settings['BATTERY_LEVEL']}%")
# 		elif not Vehicle.connect["is_connected"]:
# 			return {"complete": True,
# 					"error": f"Charging finished, OUTLET disconnected! \n BATTERY:{Vehicle.settings['BATTERY_LEVEL']}%"}
# 		else:
# 			return {"complete": False, "error": "Unexpected error!"}
# 	return {"complete": True, "error": None}
#
#
# def simulate_battery_charging(actual_battery_state, kw_per_minute):
# 	while Vehicle.settings["BATTERY_LEVEL"] < 100:
# 		if Vehicle.connect["is_connected"]:
# 			if Vehicle.settings["BATTERY_LEVEL"] >= 80:
# 				if actual_battery_state + kw_per_minute / 1.1 > Vehicle.settings["MAX_BATTERY_CAPACITY"]:
# 					last_charge_count = actual_battery_state + kw_per_minute / 1.1 - Vehicle.settings[
# 						"MAX_BATTERY_CAPACITY"]
# 					actual_battery_state += last_charge_count
# 					transfer_kw_to_percent(actual_battery_state)
# 					print(f"CHARGING ONGOING: {Vehicle.settings['BATTERY_LEVEL']}%")
# 					return {"complete": True, "error": None}
# 				actual_battery_state += kw_per_minute / 1.1
# 				transfer_kw_to_percent(actual_battery_state)
# 				time.sleep(1)
# 				print(f"CHARGING ONGOING: {Vehicle.settings['BATTERY_LEVEL']}%")
# 			else:
# 				actual_battery_state += kw_per_minute
# 				transfer_kw_to_percent(actual_battery_state)
# 				time.sleep(1)
# 				print(f"CHARGING ONGOING: {Vehicle.settings['BATTERY_LEVEL']}%")
# 		elif not Vehicle.connect["is_connected"]:
# 			return {"complete": True,
# 					"error": f"Charging finished, OUTLET disconnected! \n BATTERY:{Vehicle.settings['BATTERY_LEVEL']}%"}
# 		else:
# 			return {"complete": False, "error": "Unexpected error!"}
# 	return {"complete": True, "error": None}
#
#
# def prepare_charging():
# 	actual_battery_state = actual_capacity()
# 	target_state_of_charge_percent = target_state_of_charge()
# 	target_kwh_before_losses = transfer_percent_to_kwh(target_state_of_charge_percent)
# 	target_kwh = compensate_for_losses(target_kwh_before_losses)
# 	time_needed_in_minutes = time_needed_to_target(target_kwh)
# 	kw_per_minute = kw_per_minutes(target_kwh, time_needed_in_minutes)
# 	# to_target_complete = simulate_charging_to_target(actual_battery_state, kw_per_minute)
#
# 	# if to_target_complete["complete"] and not Charger.charging["is_finished"]:
# 	# 	simulate_charging_to_max_battery_level(actual_battery_state, kw_per_minute)
# 	simulate_battery_charging(actual_battery_state, kw_per_minute)
# 	Charger.charging["is_finished"] = True
# 	print("charging complete!")
# 	return
