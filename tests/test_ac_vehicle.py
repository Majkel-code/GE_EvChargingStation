import requests

from tests.test_configuration import TestConfigureServer


class TestAcVehicleEndpoints(TestConfigureServer):
    @classmethod
    def setUpClass(self) -> None:
        super().setUpClass()
        self.VEHICLE_URL_AC = self.test_config["VEHICLE_URL_AC"]
        self.CONNECT_AC = self.test_config["CONNECT_AC"]
        self.VEHICLE_EVERY_SETTING = self.test_config["VEHICLE_CHECK_EVERY_SETTINGS_AC"]

    def setUp(self) -> None:
        if not self.check_charger_data(
            url_charger=self.CHARGER_SERVER_URL, key_word="ac_connect"
        ).json()["ac_connect"]:
            requests.post(f"{self.CONNECT_AC}{self.test_config['VEHICLE_CONNECT_AC']}")
        else:
            pass

    def test_check_vehicle_settings(self):
        print("TEST PROPERLY TAKE VEHICLE SETTINGS!")
        response_get_vehicle_settings = requests.get(
            f"{self.VEHICLE_URL_AC}{self.test_config['VEHICLE_TAKE_ALL_AC']}"
        )
        assert response_get_vehicle_settings.status_code == 200
        geted_settings = response_get_vehicle_settings.json()
        check_data = [param for param in self.VEHICLE_EVERY_SETTING if param in geted_settings]
        assert self.VEHICLE_EVERY_SETTING == check_data

    def test_check_specific_value(self):
        self.check_vehicle_data(url_vehicle=self.VEHICLE_SERVER_URL, key_word="reload_ac")
        self.check_charger_data(url_charger=self.CHARGER_SERVER_URL, key_word="reload_settings_ac")
        print("SEND ENDPOINT FOR EVERY VEHICLE SETTINGS ONE BY ONE")
        for param in self.VEHICLE_EVERY_SETTING:
            response_take_specific_setting = requests.get(f"{self.VEHICLE_URL_AC}{param}")
            assert response_take_specific_setting.status_code == 200
            print(f"take_specific_setting response json: {response_take_specific_setting.json()}")
            print(
                f"take_specific_setting test config: {self.test_config['VEHICLE_PROPER_VALUE_AC'][f'{param}']}"
            )
            assert (
                response_take_specific_setting.json()
                == self.test_config["VEHICLE_PROPER_VALUE_AC"][f"{param}"]
            )

    def test_reconfigure_parameter(self):
        print("SEND ENDPOINT TO CHANGE SOME VALUE IN SETTINGS")
        response_edit_param = requests.put(
            f"{self.VEHICLE_URL_AC}edit",
            json=self.test_config["VEHICLE_CHANGE_VALUE_AC"],
        )
        assert response_edit_param.status_code == 200
        assert response_edit_param.json() == {"response": True, "error": None}

    # NEGATIVE TESTS FOR VEHICLE!
    def test_negative_response_reconfiguration(self):
        print("TEST NEGATIVE RECONFIGURE SETTING WITH INCORRECT VALUE!")
        negative_response_edit_param = requests.put(
            f"{self.VEHICLE_URL_AC}edit",
            json=self.test_config["VEHICLE_INCORRECT_CHANGE_VALUE_AC"],
        )
        assert negative_response_edit_param.status_code == 200
        assert negative_response_edit_param.json() == {
            "response": False,
            "error": f"{self.test_config['VEHICLE_INCORRECT_CHANGE_VALUE_AC']['key']}' CAN'T BE FIND!",
        }

    def tearDown(self) -> None:
        print("SEND DISCONNECT VEHICLE!")
        if self.check_charger_data(
            url_charger=self.CHARGER_SERVER_URL, key_word="ac_connect"
        ).json()["ac_connect"]:
            requests.post(f"{self.CONNECT_AC}{self.test_config['VEHICLE_DISCONNECT_AC']}")
