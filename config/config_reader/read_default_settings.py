import yaml


def read_charger_settings():
	with open("config/config_files/charger_config.yaml", "r+") as f:
		data = yaml.safe_load(f)
		return data


def read_vehicle_settings():
	with open("config/config_files/vehicle_config.yaml", "r+") as f:
		data = yaml.safe_load(f)
		return data