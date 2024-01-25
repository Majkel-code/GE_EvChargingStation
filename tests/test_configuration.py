import threading
import time
import unittest

import yaml

import VEHICLE.veh_config.config_reader.read_default_settings as read_default_settings_vehicle
from CHARGER.charger_server import Server as ChargerServer
from CHARGER.config import charger_vehicle_config_bridge
from CHARGER.config.config_reader import read_default_settings as read_default_settings_charger
from VEHICLE.veh_config import vehicle_config_bridge
from VEHICLE.vehicle_server import Server as VehicleServer

# cwd = os.getcwd()
# sys.path.insert(0, os.path.join(cwd, "CHARGER"))
# sys.path.insert(0, os.path.join(cwd, "VEHICLE"))

# print(os.getcwd())
# print(sys.path)


def read_tests_settings():
    with open("tests/test_config/test_configs.yaml", "r+") as f:
        test_config = yaml.safe_load(f)
    return test_config


class TestConfigureServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("load data config")
        # unittest.TestLoader.sortTestMethodsUsing = None
        cls.test_config = read_tests_settings()
        cls.CHARGER_SERVER_URL = cls.test_config["CHARGER_SERVER_URL"]
        cls.VEHICLE_SERVER_URL = cls.test_config["VEHICLE_SERVER_URL"]
        cls.AC_CONNECTED = False
        cls.CHADEMO_CONNECTED = False
        if charger_vehicle_config_bridge.IsServerAlive._is_alive_ is False:
            print("START CHARGER SERVER!")
            init_charger = ChargerServer()
            cls.thread = threading.Thread(target=init_charger.start, args=(), daemon=True)
            cls.thread.start()
            time.sleep(1)
        else:
            pass

        if vehicle_config_bridge.IsServerAlive._is_alive_ is False:
            print("START VEHICLE SERVER!")
            init_vehicle = VehicleServer()
            cls.thread = threading.Thread(target=init_vehicle.start, args=(), daemon=True)
            cls.thread.start()
            time.sleep(1)
        else:
            pass

    def read_vehicle_chademo_settings(cls):
        vehicle_config_bridge.VehicleBridge.settings_chademo = (
            read_default_settings_vehicle.read_vehicle_chademo_settings()
        )

    def read_vehicle_ac_settings(cls):
        vehicle_config_bridge.VehicleBridge.settings_ac = (
            read_default_settings_vehicle.read_vehicle_ac_settings()
        )

    def read_charger_settings(cls):
        charger_vehicle_config_bridge.ChargerBridge.settings = (
            read_default_settings_charger.read_charger_settings()
        )

    def custom_timeout_chademo(cls):
        timeout_iteration = 0
        first_check = charger_vehicle_config_bridge.ChargerBridge._energy_is_send_loop_chademo_
        while timeout_iteration < 30:
            time.sleep(1)
            if (
                first_check
                < charger_vehicle_config_bridge.ChargerBridge._energy_is_send_loop_chademo_
            ):
                return False
            elif charger_vehicle_config_bridge.ChargerBridge._charging_finished_chademo_:
                return True
            else:
                timeout_iteration += 1
        return True

    def custom_timeout_ac(cls):
        timeout_iteration = 0
        first_check = charger_vehicle_config_bridge.ChargerBridge._energy_is_send_loop_ac_
        while timeout_iteration < 30:
            time.sleep(1)
            if charger_vehicle_config_bridge.ChargerBridge._charging_finished_ac_:
                return True
            elif first_check < charger_vehicle_config_bridge.ChargerBridge._energy_is_send_loop_ac_:
                timeout_iteration = 0
                return False
            else:
                timeout_iteration += 1
        return True

    @classmethod
    def tearDownClass(cls):
        print("FUNCTION THAT SHOULD CHECK SHUTDOWN ENDPOINT // COMING SOON!")
