from charger_vehicle_config import VehicleBridge as Vehicle
from charger_vehicle_config import ChargerBridge as Charger
print(f"\033[1;30;40m Dark Gray      \033[0m 1;30;40m")
print("\033[1;31;40m Bright Red     \033[0m 1;31;40m")
print("\033[1;32;40m Bright Green   \033[0m 1;32;40m")
print("\033[1;33;40m Yellow         \033[0m 1;33;40m")
print("\033[1;34;40m Bright Blue    \033[0m 1;34;40m")
print("\033[1;35;40m Bright Magenta \033[0m 1;35;40m")
print("\033[1;36;40m Bright Cyan    \033[0m 1;36;40m")


def console_decorator(func):
	def wrapper(*args, **kwargs):
		try:
			result = func(*args, **kwargs)
			return {
				"complete": True,
				"error": []
			}
		except Exception as e:
			return {
				"result": False,
				"error": [e]
			}
	return wrapper



@console_decorator
def current_battery_status_kwh(value):
	current_battery = (value / 100) * 40
	return current_battery

@console_decorator
def current_battery(value):
	current_battery = (value / 100) * 40
	return current_battery

@console_decorator
def abc(value):
	current_battery = (value / 100) * 40
	return current_battery


def some_function():
	output = current_battery_status_kwh(5)
	print(current_battery())
	print(abc(65))
	print(output['complete'])


some_function()