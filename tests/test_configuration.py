import threading
import time
import unittest

import requests
import yaml

from CHARGER.charger_server import Server as ChargerServer
from VEHICLE.vehicle_server import Server as VehicleServer


def read_tests_settings():
    with open("tests/test_config/test_configs.yaml", "r+") as f:
        test_config = yaml.safe_load(f)
    return test_config


class TestConfigureServer(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print("load data config")
        self.test_config = read_tests_settings()
        self.CHARGER_SERVER_URL = self.test_config["CHARGER_SERVER_URL"]
        self.VEHICLE_SERVER_URL = self.test_config["VEHICLE_SERVER_URL"]

        charger_is_alive = self.check_charger_data(
            self, url_charger=self.CHARGER_SERVER_URL, key_word=self.test_config["SERVER_IS_ALIVE"]
        )
        if charger_is_alive == None:
            print("START CHARGER SERVER!")
            init_charger = ChargerServer()
            self.thread = threading.Thread(target=init_charger.start, args=(), daemon=True)
            self.thread.start()
            time.sleep(1)
        else:
            pass
        vehicle_is_alive = self.check_vehicle_data(
            self, url_vehicle=self.VEHICLE_SERVER_URL, key_word=self.test_config["SERVER_IS_ALIVE"]
        )
        if vehicle_is_alive == None:
            print("START VEHICLE SERVER!")
            init_vehicle = VehicleServer()
            self.thread = threading.Thread(target=init_vehicle.start, args=(), daemon=True)
            self.thread.start()
            time.sleep(1)
        else:
            pass

    def check_charger_data(self, url_charger, key_word):
        url = f"{url_charger}{key_word}"
        headers = {"Content-Type": "application/json"}
        response = requests.get(url, headers=headers)
        if response.ok:
            return response

    def check_vehicle_data(self, url_vehicle, key_word):
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
            if (
                first_check_flow["chademo_charging_ongoing"]
                < check_flow["chademo_charging_ongoing"]
            ):
                return False
            elif self.check_charger_data(
                url_charger=self.CHARGER_SERVER_URL, key_word="chademo_finished"
            ).json()["chademo_finished"]:
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
            elif self.check_charger_data(
                url_charger=self.CHARGER_SERVER_URL, key_word="ac_finished"
            ).json()["ac_finished"]:
                timeout_iteration = 0
                return True
            else:
                timeout_iteration += 1
        return True

    @classmethod
    def tearDownClass(self):
        print("FUNCTION THAT SHOULD CHECK SHUTDOWN ENDPOINT // COMING SOON!")
