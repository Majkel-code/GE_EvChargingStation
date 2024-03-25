import requests

from tests.test_configuration import TestConfigureServer


class TestComboChargingSession(TestConfigureServer):
    @classmethod
    def setUpClass(self) -> None:
        super().setUpClass()
        self.CHARGER_URL = self.test_config["CHARGER_URL"]
        self.CONNECT_AC = self.test_config["CONNECT_AC"]
        self.CONNECT_CHADEMO = self.test_config["CONNECT_CHADEMO"]
        self.VEHICLE_URL_AC = self.test_config["VEHICLE_URL_AC"]
        self.VEHICLE_URL_CHADEMO = self.test_config["VEHICLE_URL_CHADEMO"]

    def setUp(self) -> None:
        if not self.check_charger_data(
            url_charger=self.CHARGER_SERVER_URL, key_word="ac_connect"
        ).json()["ac_connect"]:
            requests.post(f"{self.CONNECT_AC}{self.test_config['VEHICLE_CONNECT_AC']}")
        if not self.check_charger_data(
            url_charger=self.CHARGER_SERVER_URL, key_word="chademo_connect"
        ).json()["chademo_connect"]:
            requests.post(f"{self.CONNECT_CHADEMO}{self.test_config['VEHICLE_CONNECT_CHADEMO']}")

    def test_reconfigure_parameter(self):
        print("SEND ENDPOINT TO CHANGE SOME VALUE IN SETTINGS")
        # chademo
        response_edit_param_chademo = requests.put(
            url=f"{self.VEHICLE_URL_CHADEMO}edit",
            json=self.test_config["VEHICLE_CHANGE_VALUE_CHADEMO"],
        )
        assert response_edit_param_chademo.status_code == 200
        assert response_edit_param_chademo.json() == {
            "response": True,
            "error": None,
        }
        # ac
        response_edit_param_ac = requests.put(
            url=f"{self.VEHICLE_URL_AC}edit",
            json=self.test_config["VEHICLE_CHANGE_VALUE_AC"],
        )
        assert response_edit_param_ac.status_code == 200
        assert response_edit_param_ac.json() == {
            "response": True,
            "error": None,
        }

    def test_session_start(self):
        self.check_charger_data(url_charger=self.CHARGER_SERVER_URL, key_word="reload_settings_ac")
        self.check_charger_data(
            url_charger=self.CHARGER_SERVER_URL, key_word="reload_settings_chademo"
        )
        requests.put(
            f"{self.VEHICLE_URL_CHADEMO}edit",
            json=self.test_config["VEHICLE_START_BATTERY_LEVEL_CHADEMO"],
        )
        requests.put(
            f"{self.VEHICLE_URL_AC}edit",
            json=self.test_config["VEHICLE_START_BATTERY_LEVEL_AC"],
        )
        print("CHECK COMBO SESSIONS FLOW AND PROPERLY COMPLETE")
        if (
            self.test_config["START_SESSION_CUSTOM_PERCENT_CHADEMO"] is not None
            and self.test_config["START_SESSION_CUSTOM_PERCENT_AC"] is not None
        ):
            start_session_url_chademo = f"{self.CHARGER_URL}{self.test_config['START_SESSION_CHADEMO']}_chademo_{self.test_config['START_SESSION_CUSTOM_PERCENT_CHADEMO']}"
            start_session_url_ac = f"{self.CHARGER_URL}{self.test_config['START_SESSION_AC']}_ac_{self.test_config['START_SESSION_CUSTOM_PERCENT_AC']}"
        else:
            start_session_url_chademo = (
                f"{self.CHARGER_URL}{self.test_config['START_SESSION_CHADEMO']}_chademo"
            )
            start_session_url_ac = f"{self.CHARGER_URL}{self.test_config['START_SESSION_AC']}_ac"
        response_session_chademo = requests.post(start_session_url_chademo)
        assert response_session_chademo.status_code == 200
        assert response_session_chademo.json() == {
            "response": True,
            "error": None,
        }
        response_session_ac = requests.post(start_session_url_ac)
        assert response_session_ac.status_code == 200
        assert response_session_ac.json() == {"response": True, "error": None}
        while True:
            if self.custom_timeout_chademo() is True and self.custom_timeout_ac() is True:
                assert (
                    self.check_charger_data(
                        url_charger=self.CHARGER_SERVER_URL, key_word="ac_finished"
                    ).json()["ac_finished"]
                    is True
                )
                assert (
                    self.check_charger_data(
                        url_charger=self.CHARGER_SERVER_URL, key_word="chademo_finished"
                    ).json()["chademo_finished"]
                    is True
                )
                break

    def test_vehicle_state_saved(self):
        self.test_session_start()
        print("CHECK SETTINGS AFTER COMBO SESSIONS SAVE PROPERLY!")
        response_check_setting = requests.get(
            f"{self.VEHICLE_URL_CHADEMO}{self.test_config['VEHICLE_TAKE_SPECIFIC_KEY_CHADEMO']}"
        )
        assert response_check_setting.status_code == 200
        assert (
            response_check_setting.json()
            > self.test_config["VEHICLE_CHANGE_VALUE_CHADEMO"]["value"]
        )
        response_check_setting = requests.get(
            f"{self.VEHICLE_URL_AC}{self.test_config['VEHICLE_TAKE_SPECIFIC_KEY_AC']}"
        )
        assert response_check_setting.status_code == 200
        assert response_check_setting.json() > self.test_config["VEHICLE_CHANGE_VALUE_AC"]["value"]

    def tearDown(self) -> None:
        if self.check_charger_data(
            url_charger=self.CHARGER_SERVER_URL, key_word="chademo_connect"
        ).json()["chademo_connect"]:
            requests.post(
                f"{self.VEHICLE_URL_CHADEMO}{self.test_config['VEHICLE_DISCONNECT_CHADEMO']}"
            )
        else:
            pass
        if self.check_charger_data(
            url_charger=self.CHARGER_SERVER_URL, key_word="ac_connect"
        ).json()["ac_connect"]:
            requests.post(f"{self.VEHICLE_URL_AC}{self.test_config['VEHICLE_CONNECT_AC']}")
        else:
            pass
