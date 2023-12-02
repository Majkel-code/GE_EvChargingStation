import requests
from tests.test_ac_vehicle import TestAcVehicleEndpoints
from config import charger_vehicle_config_bridge
import time

class TestAcChargingSession(TestAcVehicleEndpoints):
    @classmethod
    def setUpClass(self) -> None:
        super().setUpClass()
        print('charging session')
        #VEHICLE and CHARGER SETTINGS FOR NOW
        self.CHARGER_URL = self.test_config['CHARGER_URL']
        # self.VEHICLE_URL = self.test_config['VEHICLE_URL']
        # self.VEHICLE_EVERY_SETTING = self.test_config['VEHICLE_CHECK_EVERY_SETTINGS']

    def setUp(self) -> None:
        if not charger_vehicle_config_bridge.VehicleBridge._connected_ac_:
            response_connect = requests.post(f'{self.VEHICLE_URL_AC}{self.test_config['VEHICLE_CONNECT_AC']}')
        else: pass

    def test_reconfigure_parameter(self):
        print('SEND ENDPOINT TO CHANGE SOME VALUE IN SETTINGS')
        response_edit_param = requests.put(self.VEHICLE_URL_AC, json=self.test_config['VEHICLE_CHANGE_VALUE_AC'])
        assert response_edit_param.status_code == 200
        print(response_edit_param.json())
        assert response_edit_param.json() == {"response": True, "error": None}   
    
    def test_session_start(self):
        self.read_vehicle_ac_settings()
        requests.put(self.VEHICLE_URL_AC, json=self.test_config['VEHICLE_START_BATTERY_LEVEL_AC'])
        print('CHECK SESSION FLOW AND PROPERLY COMPLETE')
        if self.test_config['START_SESSION_CUSTOM_PERCENT_AC'] is not None:
            start_session_url = f'{self.CHARGER_URL}{self.test_config['START_SESSION_AC']}_ac_{self.test_config['START_SESSION_CUSTOM_PERCENT_AC']}'
        else:
            start_session_url = f'{self.CHARGER_URL}{self.test_config['START_SESSION_AC']}_ac'
        response_session = requests.post(start_session_url)
        assert response_session.status_code == 200
        assert response_session.json() == {"response": True, "error": None}
        while True:
            if self.custom_timeout_ac():
                assert charger_vehicle_config_bridge.ChargerBridge._charging_finished_ac_ == True
                break

    def test_vehicle_state_saved(self):
        self.test_session_start()
        print('CHECK SETTINGS AFTER SESSION SAVE PROPERLY!')
        response_check_setting = requests.get(f'{self.VEHICLE_URL_AC}{self.test_config['VEHICLE_TAKE_SPECIFIC_KEY_AC']}')
        assert response_check_setting.status_code == 200
        assert response_check_setting.json() > self.test_config['VEHICLE_CHANGE_VALUE_AC']['value']

    def tearDown(self) -> None:
        if charger_vehicle_config_bridge.VehicleBridge._connected_ac_:
            response_disconnect_vehicle = requests.post(F'{self.VEHICLE_URL_AC}{self.test_config['VEHICLE_DISCONNECT_AC']}')
        else: pass

    @classmethod
    def tearDownClass(self) -> None:
        super().tearDownClass()