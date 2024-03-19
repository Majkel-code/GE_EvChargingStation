import requests

from tests.test_chademo_vehicle import TestChademoVehicleEndpoints


class TestChademoChargingSession(TestChademoVehicleEndpoints):
    @classmethod
    def setUpClass(self) -> None:
        super().setUpClass()
        print("charging session")
        self.CHARGER_URL = self.test_config["CHARGER_URL"]

    def setUp(self) -> None:
        if not self.check_charger_data(
            url_charger=self.CHARGER_SERVER_URL, key_word="chademo_connect"
        ).json()["chademo_connect"]:
            requests.post(f"{self.CONNECT_CHADEMO}{self.test_config['VEHICLE_CONNECT_CHADEMO']}")

    def test_reconfigure_parameter(self):
        print("SEND ENDPOINT TO CHANGE SOME VALUE IN SETTINGS")
        response_edit_param = requests.put(
            f"{self.VEHICLE_URL_CHADEMO}edit",
            json=self.test_config["VEHICLE_CHANGE_VALUE_CHADEMO"],
        )
        assert response_edit_param.status_code == 200
        print(response_edit_param.json())
        assert response_edit_param.json() == {"response": True, "error": None}

    def test_session_start(self):
        self.check_charger_data(
            url_charger=self.CHARGER_SERVER_URL, key_word="reload_settings_chademo"
        )
        requests.put(
            f"{self.VEHICLE_URL_CHADEMO}edit",
            json=self.test_config["VEHICLE_START_BATTERY_LEVEL_CHADEMO"],
        )
        print("CHECK SESSION FLOW AND PROPERLY COMPLETE")
        if self.test_config["START_SESSION_CUSTOM_PERCENT_CHADEMO"] is not None:
            start_session_url = f"{self.CHARGER_URL}{self.test_config['START_SESSION_CHADEMO']}_chademo_{self.test_config['START_SESSION_CUSTOM_PERCENT_CHADEMO']}"
        else:
            start_session_url = (
                f"{self.CHARGER_URL}{self.test_config['START_SESSION_CHADEMO']}_chademo"
            )

        response_session = requests.post(start_session_url)
        assert response_session.status_code == 200
        assert response_session.json() == {"response": True, "error": None}
        while True:
            if self.custom_timeout_chademo() is True:
                assert (
                    self.check_charger_data(
                        url_charger=self.CHARGER_SERVER_URL, key_word="chademo_finished"
                    ).json()["chademo_finished"]
                    is True
                )
                break

    def test_vehicle_state_saved(self):
        self.test_session_start()
        print("CHECK SETTINGS AFTER SESSION SAVE PROPERLY!")
        response_check_setting = requests.get(
            f"{self.VEHICLE_URL_CHADEMO}{self.test_config['VEHICLE_TAKE_SPECIFIC_KEY_CHADEMO']}"
        )
        assert response_check_setting.status_code == 200
        assert (
            response_check_setting.json()
            > self.test_config["VEHICLE_CHANGE_VALUE_CHADEMO"]["value"]
        )

    def tearDown(self) -> None:
        if self.check_charger_data(
            url_charger=self.CHARGER_SERVER_URL, key_word="chademo_connect"
        ).json()["chademo_connect"]:
            requests.post(
                f"{self.VEHICLE_URL_CHADEMO}{self.test_config['VEHICLE_DISCONNECT_CHADEMO']}"
            )
