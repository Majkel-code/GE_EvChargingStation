import requests

from tests.test_configuration import TestConfigureServer


class TestChademoVehicleEndpoints(TestConfigureServer):
    @classmethod
    def setUpClass(self) -> None:
        super().setUpClass()
        self.VEHICLE_URL_CHADEMO = self.test_config["VEHICLE_URL_CHADEMO"]
        self.CONNECT_CHADEMO = self.test_config["CONNECT_CHADEMO"]
        self.VEHICLE_EVERY_SETTING = self.test_config["VEHICLE_CHECK_EVERY_SETTINGS_CHADEMO"]

    def setUp(self) -> None:
        if not self.check_charger_data(
            url_charger=self.CHARGER_SERVER_URL, key_word="chademo_connect"
        ).json()["chademo_connect"]:
            requests.post(f"{self.CONNECT_CHADEMO}{self.test_config['VEHICLE_CONNECT_CHADEMO']}")

    def test_check_vehicle_settings(self):
        print("TEST PROPERLY TAKE VEHICLE SETTINGS!")
        response_get_vehicle_settings = requests.get(
            f"{self.VEHICLE_URL_CHADEMO}{self.test_config['VEHICLE_TAKE_ALL_CHADEMO']}"
        )
        assert response_get_vehicle_settings.status_code == 200
        geted_settings = response_get_vehicle_settings.json()
        check_data = [param for param in self.VEHICLE_EVERY_SETTING if param in geted_settings]
        assert self.VEHICLE_EVERY_SETTING == check_data

    def test_check_specific_value(self):
        self.check_vehicle_data(url_vehicle=self.VEHICLE_SERVER_URL, key_word="reload_chademo")
        self.check_charger_data(
            url_charger=self.CHARGER_SERVER_URL, key_word="reload_settings_chademo"
        )
        print("SEND ENDPOINT FOR EVERY VEHICLE SETTINGS ONE BY ONE")
        for param in self.VEHICLE_EVERY_SETTING:
            response_take_specific_setting = requests.get(f"{self.VEHICLE_URL_CHADEMO}{param}")
            assert response_take_specific_setting.status_code == 200
            print(f"take_specific_setting response json: {response_take_specific_setting.json()}")
            print(
                f"take_specific_setting test config: {self.test_config[f'VEHICLE_PROPER_VALUE_CHADEMO'][f'{param}']}"
            )
            assert (
                response_take_specific_setting.json()
                == self.test_config["VEHICLE_PROPER_VALUE_CHADEMO"][f"{param}"]
            )

    def test_reconfigure_parameter(self):
        print("SEND ENDPOINT TO CHANGE SOME VALUE IN SETTINGS")
        response_edit_param = requests.put(
            f"{self.VEHICLE_URL_CHADEMO}edit",
            json=self.test_config["VEHICLE_CHANGE_VALUE_CHADEMO"],
        )
        assert response_edit_param.status_code == 200
        assert response_edit_param.json() == {"response": True, "error": None}

    # NEGATIVE TESTS FOR VEHICLE!
    def test_negative_response_reconfiguration(self):
        print("TEST NEGATIVE RECONFIGURE SETTING WITH INCORRECT VALUE!")
        negative_response_edit_param = requests.put(
            f"{self.VEHICLE_URL_CHADEMO}edit",
            json=self.test_config["VEHICLE_INCORRECT_CHANGE_VALUE_CHADEMO"],
        )
        assert negative_response_edit_param.status_code == 200
        assert negative_response_edit_param.json() == {
            "response": False,
            "error": f"{self.test_config['VEHICLE_INCORRECT_CHANGE_VALUE_CHADEMO']['key']}' CAN'T BE FIND!",
        }

    # def test_negative_read_setting_before_connection(self):
    #     requests.post(f"{self.VEHICLE_URL_CHADEMO}{self.test_config['VEHICLE_DISCONNECT_CHADEMO']}")
    #     print("TEST NEGATIVE TAKE CHARGER SETTING BEFORE CONNECTION!")
    #     negative_response_get_vehicle_settings = requests.get(
    #         f"{self.VEHICLE_URL_CHADEMO}{self.test_config['VEHICLE_TAKE_SPECIFIC_KEY_CHADEMO']}"
    #     )
    #     assert negative_response_get_vehicle_settings.status_code != 200
    #     assert negative_response_get_vehicle_settings.json() == {
    #         "detail": f"'{self.test_config['VEHICLE_TAKE_SPECIFIC_KEY_CHADEMO']}' CAN'T BE FIND!"
    #     }

    def tearDown(self) -> None:
        print("SEND DISCONNECT VEHICLE!")
        if self.check_charger_data(
            url_charger=self.CHARGER_SERVER_URL, key_word="chademo_connect"
        ).json()["chademo_connect"]:
            requests.post(
                f"{self.VEHICLE_URL_CHADEMO}{self.test_config['VEHICLE_DISCONNECT_CHADEMO']}"
            )
