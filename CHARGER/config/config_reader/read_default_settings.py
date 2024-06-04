from pathlib import Path

import yaml

current_path = Path(__file__).absolute().parents[1]


def read_charger_settings():
    with open(f"{current_path}/config_files/charger_config.yaml", "r+") as f:
        data = yaml.safe_load(f)
        return data
