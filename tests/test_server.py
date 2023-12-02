import unittest
import threading
import yaml
import requests
import time
from Server import Server
import config.config_reader.read_default_settings as read_default_settings
from config import charger_vehicle_config_bridge


def read_tests_settings():
    with open("tests/test_configs.yaml", "r+") as f:
        test_config = yaml.safe_load(f)
    return test_config

class TestConfigureServer(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print('load data config')
        unittest.TestLoader.sortTestMethodsUsing = None
        self.test_config = read_tests_settings()
        self.SERVER_URL = self.test_config['SERVER_URL']
        request = requests.get(f'{self.SERVER_URL}is_alive')
        if request.status_code != 200:
            print('START FASTAPI SERVER!')
            start = Server()
            self.thread = threading.Thread(target=start.start,args=(), daemon=True)
            self.thread.start()
            time.sleep(1)
        else:
            pass

    def read_vehicle_chademo_settings(self):
        charger_vehicle_config_bridge.VehicleBridge.settings_chademo = read_default_settings.read_vehicle_chademo_settings()
    
    def read_vehicle_ac_settings(self):
        charger_vehicle_config_bridge.VehicleBridge.settings_ac = read_default_settings.read_vehicle_ac_settings()

    def read_charger_settings(self):
        charger_vehicle_config_bridge.ChargerBridge.settings = read_default_settings.read_charger_settings()

    def custom_timeout_chademo(self):
        timeout_iteration = 0
        first_check = charger_vehicle_config_bridge.ChargerBridge._energy_is_send_loop_chademo_
        while timeout_iteration < 30:
            time.sleep(1)
            if first_check < charger_vehicle_config_bridge.ChargerBridge._energy_is_send_loop_chademo_:
                return False
            elif charger_vehicle_config_bridge.ChargerBridge._charging_finished_chademo_:
                return True
            else:
                timeout_iteration += 1
        return True
    
    def custom_timeout_ac(self):
        timeout_iteration = 0
        first_check = charger_vehicle_config_bridge.ChargerBridge._energy_is_send_loop_chademo_
        while timeout_iteration < 30:
            time.sleep(1)
            if first_check < charger_vehicle_config_bridge.ChargerBridge._energy_is_send_loop_chademo_:
                return False
            elif charger_vehicle_config_bridge.ChargerBridge._charging_finished_chademo_:
                return True
            else:
                timeout_iteration += 1
        return True

    @classmethod
    def tearDownClass(self):
        print('FUNCTION THAT SHOULD CHECK SHUTDOWN ENDPOINT // COMING SOON!')
        shut_down = requests.get(f'{self.test_config['SERVER_URL']}/something_stopped')
        assert shut_down.status_code == 404
        # shut_down = requests.get('http://127.0.0.1:5000/server_stop')
        # print(shut_down.json())
        # assert shut_down.json() == {"response": True, "error": None}
        # time.sleep(10)
   
class TestServer(TestConfigureServer):
    @classmethod
    def setUpClass(self) -> None:
        super().setUpClass()
        print('server test')

    def test_server_is_alive(self):
        print('TEST SERVER IS ALIVE!')
        request = requests.get(f'{self.SERVER_URL}{self.test_config['SERVER_IS_ALIVE']}')
        assert request.status_code == 200
        assert request.json() == {"is_alive": True, "error": None}

    @classmethod
    def tearDownClass(self) -> None:
        super().tearDownClass()        
