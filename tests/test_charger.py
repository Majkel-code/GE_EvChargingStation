import requests
from tests.test_server import TestConfigureServer

class TestChargerEndpoints(TestConfigureServer):
    @classmethod
    def setUpClass(self) -> None:
        super().setUpClass()
        self.CHARGER_URL = self.test_config['CHARGER_URL']
        self.CHARGER_EVERY_SETTING = self.test_config['CHARGER_CHECK_EVERY_SETTING']
        print('charger')

    def test_check_charger_settings(self):
        print("TEST PROPERLY TAKE CHARGER SETTINGS!")
        response_get_charger_settings = requests.get(f"{self.CHARGER_URL}{self.test_config['CHARGER_TAKE_ALL']}")
        assert response_get_charger_settings.status_code == 200
        geted_settings = response_get_charger_settings.json()
        check_data = [param for param in self.CHARGER_EVERY_SETTING if param in geted_settings]
        assert self.CHARGER_EVERY_SETTING == check_data

    def test_check_specific_value(self):
        self.read_charger_settings()
        for param in self.CHARGER_EVERY_SETTING:
            response_take_specific_setting = requests.get(f'{self.CHARGER_URL}{param}')
            assert response_take_specific_setting.status_code == 200
            print(f"take_specific_setting response json: {response_take_specific_setting.json()}")
            print(f"take_specific_setting test config: {self.test_config['CHARGER_PROPER_VALUE'][f'{param}']}")
            assert response_take_specific_setting.json() == self.test_config[f'CHARGER_PROPER_VALUE'][f'{param}']

    def test_change_param(self):
        print("CHNAGE PARAM IN CHARGER CONFIGURATION")
        response_edit_param = requests.put(self.CHARGER_URL, json=self.test_config['CHARGER_CHANGE_VALUE'])
        assert response_edit_param.status_code == 200
        print(response_edit_param.json())
        print(f"{self.test_config['CHARGER_CHANGE_VALUE']['key']}={self.test_config['CHARGER_CHANGE_VALUE']['value']}")
        assert response_edit_param.json() == {"response": True, "error": None}

    @classmethod
    def tearDownClass(self) -> None:
        super().tearDownClass()
