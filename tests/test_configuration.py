import subprocess
import time
import unittest
from pathlib import Path
import os

import requests
import yaml


def read_tests_settings():
    with open("tests/test_config/test_configs.yaml", "r+") as f:
        test_config = yaml.safe_load(f)
    return test_config


current_path = Path(__file__).absolute().parents[1]


def read_local_key(key_path):
    if os.path.exists(key_path):
        with open(key_path, "r") as f:
            return f.read()


class TestConfigureServer(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print("load data config")
        self.test_config = read_tests_settings()
        self.CHARGER_SERVER_URL = self.test_config["CHARGER_SERVER_URL"]
        self.VEHICLE_SERVER_URL = self.test_config["VEHICLE_SERVER_URL"]
        self.AUTH_KEY_PATH = self.test_config["AUTHORIZATION_KEY_SAVE_PATH"]

        current_path = Path(__file__).absolute().parents[1]
        charger_path = f"{current_path}/CHARGER/charger_server.py"
        vehicle_path = f"{current_path}/VEHICLE/vehicle_server.py"
        self.procs = []
        if self.CHARGER_SERVER_URL == "http://127.0.0.1:5000/":
            self.procs.append(subprocess.Popen(["python3", f"{charger_path}"]))
        if self.VEHICLE_SERVER_URL == "http://127.0.0.1:5001/":
            self.procs.append(subprocess.Popen(["python3", f"{vehicle_path}"]))
 
        self.AUTH_KEY = read_local_key(self.AUTH_KEY_PATH)

    def check_charger_data(self, url_charger, key_word):
        time.sleep(1)
        url = f"{url_charger}{key_word}"
        headers = {"Content-Type": "application/json", "AUTHORIZATION": self.AUTH_KEY}
        response = requests.get(url, headers=headers)
        if response.ok:
            return response

    def check_vehicle_data(self, url_vehicle, key_word):
        time.sleep(1)
        url = f"{url_vehicle}{key_word}"
        headers = {"Content-Type": "application/json"}
        response = requests.get(url, headers=headers)
        if response.ok:
            return response

    def custom_timeout_chademo(self):
        timeout_iteration = 0
        first_check_flow = self.check_charger_data(
            url_charger=self.CHARGER_SERVER_URL, key_word="chademo_charging_ongoing"
        ).json()
        while timeout_iteration < 30:
            time.sleep(1)
            check_flow = self.check_charger_data(
                url_charger=self.CHARGER_SERVER_URL, key_word="chademo_charging_ongoing"
            ).json()
            if first_check_flow["chademo_charging_ongoing"] < check_flow["chademo_charging_ongoing"]:
                return False
            elif self.check_charger_data(url_charger=self.CHARGER_SERVER_URL, key_word="chademo_finished").json()[
                "chademo_finished"
            ]:
                timeout_iteration = 0
                return True
            else:
                timeout_iteration += 1
        return True

    def custom_timeout_ac(self):
        timeout_iteration = 0
        first_check_flow = self.check_charger_data(
            url_charger=self.CHARGER_SERVER_URL, key_word="ac_charging_ongoing"
        ).json()
        while timeout_iteration < 30:
            time.sleep(1)
            check_flow = self.check_charger_data(
                url_charger=self.CHARGER_SERVER_URL, key_word="ac_charging_ongoing"
            ).json()
            if first_check_flow["ac_charging_ongoing"] < check_flow["ac_charging_ongoing"]:
                return False
            elif self.check_charger_data(url_charger=self.CHARGER_SERVER_URL, key_word="ac_finished").json()[
                "ac_finished"
            ]:
                timeout_iteration = 0
                return True
            else:
                timeout_iteration += 1
        return True

    @classmethod
    def tearDownClass(self):
        print("FUNCTION THAT SHOULD CHECK SHUTDOWN ENDPOINT // COMING SOON!")
        for p in self.procs:
            p.terminate()
            p.wait()
        
            
