import yaml
from pathlib import Path

current_path = Path(__file__).absolute().parents[1]

def read_vehicle_chademo_settings():
    with open(f"{current_path}/config_files/vehicle_chademo_config.yaml", "r+") as f:
        data = yaml.safe_load(f)
        return data


def read_vehicle_ac_settings():
    with open(f"{current_path}/config_files/vehicle_ac_config.yaml", "r+") as f:
        data = yaml.safe_load(f)
        return data
