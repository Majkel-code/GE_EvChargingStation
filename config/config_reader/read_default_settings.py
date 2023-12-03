import yaml


def read_charger_settings():
    with open("config/config_files/charger_config.yaml", "r+") as f:
        data = yaml.safe_load(f)
        return data


def read_vehicle_chademo_settings():
    with open("config/config_files/vehicle_chademo_config.yaml", "r+") as f:
        data = yaml.safe_load(f)
        return data


def read_vehicle_ac_settings():
    with open("config/config_files/vehicle_ac_config.yaml", "r+") as f:
        data = yaml.safe_load(f)
        return data
