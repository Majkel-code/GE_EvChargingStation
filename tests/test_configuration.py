import threading
import time
import unittest

import yaml

import CHARGER.config.config_reader.read_default_settings as read_default_settings
from CHARGER.charger_server import Server as ChargerServer
from CHARGER.config import charger_vehicle_config_bridge


def read_tests_settings():
    with open("tests/test_config/test_configs.yaml", "r+") as f:
        test_config = yaml.safe_load(f)
    return test_config


class TestConfigureServer(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print("load data config")
        unittest.TestLoader.sortTestMethodsUsing = None
        self.test_config = read_tests_settings()
        self.CHARGER_SERVER_URL = self.test_config["CHARGER_SERVER_URL"]
        if charger_vehicle_config_bridge.IsServerAlive._is_alive_ == False:
            print("START CHARGER SERVER!")
            start = ChargerServer()
            self.thread = threading.Thread(
                target=start.start, args=(), daemon=True
            )
            self.thread.start()
            time.sleep(1)

        else:
            pass
        # if vehicle_bridge.IsServerAlive._is_alive_ == False:
        #     print("START VEHICLE SERVER!")
        #     start = VehicleServer()
        #     self.thread = threading.Thread(target=start.start, args=(), daemon=True)
        #     self.thread.start()
        #     time.sleep(1)
        # else: pass

    # def read_vehicle_chademo_settings(self):
    #     charger_vehicle_config_bridge.VehicleBridge.settings_chademo = (
    #         read_default_settings.read_vehicle_chademo_settings()
    #     )

    # def read_vehicle_ac_settings(self):
    #     charger_vehicle_config_bridge.VehicleBridge.settings_ac = read_default_settings.read_vehicle_ac_settings()

    def read_charger_settings(self):
        charger_vehicle_config_bridge.ChargerBridge.settings = (
            read_default_settings.read_charger_settings()
        )

    def custom_timeout_chademo(self):
        timeout_iteration = 0
        first_check = (
            charger_vehicle_config_bridge.ChargerBridge._energy_is_send_loop_chademo_
        )
        while timeout_iteration < 30:
            time.sleep(1)
            if (
                first_check
                < charger_vehicle_config_bridge.ChargerBridge._energy_is_send_loop_chademo_
            ):
                return False
            elif (
                charger_vehicle_config_bridge.ChargerBridge._charging_finished_chademo_
            ):
                return True
            else:
                timeout_iteration += 1
        return True

    def custom_timeout_ac(self):
        timeout_iteration = 0
        first_check = (
            charger_vehicle_config_bridge.ChargerBridge._energy_is_send_loop_chademo_
        )
        while timeout_iteration < 30:
            time.sleep(1)
            if (
                first_check
                < charger_vehicle_config_bridge.ChargerBridge._energy_is_send_loop_chademo_
            ):
                return False
            elif (
                charger_vehicle_config_bridge.ChargerBridge._charging_finished_chademo_
            ):
                return True
            else:
                timeout_iteration += 1
        return True

    @classmethod
    def tearDownClass(self):
        print("FUNCTION THAT SHOULD CHECK SHUTDOWN ENDPOINT // COMING SOON!")
