import datetime
import json
import os
import os.path
from pathlib import Path

current_path = Path(__file__).absolute().parents[2]
today = datetime.date.today()


class SessionSaver:
    def __init__(self) -> None:
        self.ac_path = f"{current_path}/veh_logs/charging_history/AC/ac_history.json"
        self.ac_history_file = {"AC": []}
        self.ac_history = {
            f"{today}": {
                "SESSION_ID": None,
                "BATTERY_LEVEL": None,
                "CHARGED_KW": None,
                "CHARGE_TIME": None,
            },
        }
        self.chademo_path = f"{current_path}/veh_logs/charging_history/CHADEMO/chademo_history.json"
        self.chademo_history_file = {"CHADEMO": []}
        self.chademo_history = {
            f"{today}": {
                "SESSION_ID": None,
                "BATTERY_LEVEL": None,
                "CHARGED_KW": None,
                "CHARGE_TIME": None,
            },
        }

        self.setup()

    def setup(self):
        if os.path.exists(self.ac_path):
            with open(self.ac_path, "r") as f:
                self.ac_history_file = json.load(f)
        else:
            with open(self.ac_path, "a") as f:
                f.write(json.dumps(self.ac_history_file))

        if os.path.exists(self.chademo_path):
            with open(self.chademo_path, "r") as f:
                self.chademo_history_file = json.load(f)
        else:
            with open(self.chademo_path, "a") as f:
                f.write(json.dumps(self.chademo_history_file))

    def open_session_history(self, outlet):
        if outlet == "AC":
            with open(self.ac_path, "r") as f:
                return json.load(f)
        elif outlet == "CHADEMO":
            with open(self.chademo_path, "r") as f:
                return json.load(f)

    def check_save_history_record(self, outlet, current_session_id, current_battery):
        if outlet == "AC":
            with open(self.ac_path, "r+") as f:
                data = json.load(f)
                if len(data[outlet]) > 0:
                    if f"{today}" not in data[outlet][0]:
                        return True
                    if (
                        data[outlet][0][f"{today}"]["SESSION_ID"] == current_session_id
                        and data[outlet][0][f"{today}"]["BATTERY_LEVEL"] < current_battery
                    ):
                        return True
                    if (
                        data[outlet][0][f"{today}"]["SESSION_ID"] == current_session_id
                        or current_session_id is None
                    ):
                        return False
                    elif data[outlet][0] != self.ac_history:
                        return True
                    else:
                        return False
                else:
                    return True
        if outlet == "CHADEMO":
            with open(self.chademo_path, "r+") as f:
                data = json.load(f)
                if len(data[outlet]) > 0:
                    if f"{today}" not in data[outlet][0]:
                        return True
                    if (
                        data[outlet][0][f"{today}"]["SESSION_ID"] == current_session_id
                        and data[outlet][0][f"{today}"]["BATTERY_LEVEL"] < current_battery
                    ):
                        return True
                    if (
                        data[outlet][0][f"{today}"]["SESSION_ID"] == current_session_id
                        or current_session_id is None
                    ):
                        return False
                    elif data[outlet][0] != self.chademo_history:
                        return True
                    else:
                        return False
                else:
                    return True

    def save_session(self, outlet, session_id, battery, charged_kw, time):
        if outlet == "AC":
            self.ac_history[f"{today}"]["SESSION_ID"] = session_id
            self.ac_history[f"{today}"]["BATTERY_LEVEL"] = battery
            self.ac_history[f"{today}"]["CHARGED_KW"] = charged_kw
            self.ac_history[f"{today}"]["CHARGE_TIME"] = time
            if self.check_save_history_record(
                outlet=outlet, current_session_id=session_id, current_battery=battery
            ):
                with open(self.ac_path, "r+") as f:
                    self.ac_history_file["AC"].insert(0, self.ac_history)
                    f.write(json.dumps(self.ac_history_file))

        elif outlet == "CHADEMO":
            self.chademo_history[f"{today}"]["SESSION_ID"] = session_id
            self.chademo_history[f"{today}"]["BATTERY_LEVEL"] = battery
            self.chademo_history[f"{today}"]["CHARGED_KW"] = charged_kw
            self.chademo_history[f"{today}"]["CHARGE_TIME"] = time
            if self.check_save_history_record(
                outlet, current_session_id=session_id, current_battery=battery
            ):
                with open(self.chademo_path, "r+") as f:
                    self.chademo_history_file["CHADEMO"].insert(0, self.chademo_history)
                    f.write(json.dumps(self.chademo_history_file))
