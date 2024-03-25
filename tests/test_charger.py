import requests
import time

from tests.test_configuration import TestConfigureServer


class TestChargerEndpoints(TestConfigureServer):
    @classmethod
    def setUpClass(self) -> None:
        super().setUpClass()
        time.sleep(2)
        self.CHARGER_URL = self.test_config["CHARGER_URL"]
        self.CHARGER_EVERY_SETTING = self.test_config["CHARGER_CHECK_EVERY_SETTING"]
        print("charger")


    def setUp(self) -> None:
        return super().setUp()

    def test_check_charger_settings(self):
        print("TEST PROPERLY TAKE CHARGER SETTINGS!")
        response_get_charger_settings = requests.get(
            f"{self.CHARGER_URL}{self.test_config['CHARGER_TAKE_ALL']}"
        )
        assert response_get_charger_settings.status_code == 200
        geted_settings = response_get_charger_settings.json()
        check_data = [param for param in self.CHARGER_EVERY_SETTING if param in geted_settings]
        assert self.CHARGER_EVERY_SETTING == check_data

    def test_check_specific_value(self):
        for param in self.CHARGER_EVERY_SETTING:
            response_take_specific_setting = requests.get(f"{self.CHARGER_URL}get/{param}")
            assert response_take_specific_setting.status_code == 200
            assert (
                response_take_specific_setting.json()
                == self.test_config["CHARGER_PROPER_VALUE"][f"{param}"]
            )

    def test_change_param(self):
        print("CHNAGE PARAM IN CHARGER CONFIGURATION")
        response_edit_param = requests.put(
            self.CHARGER_URL, json=self.test_config["CHARGER_CHANGE_VALUE"]
        )
        assert response_edit_param.status_code == 200
        assert response_edit_param.json() == {"response": True, "error": None}

    @classmethod
    def tearDownClass(self) -> None:
        super().tearDownClass()
