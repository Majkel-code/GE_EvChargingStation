import datetime

import requests

from tests.test_configuration import TestConfigureServer

today = datetime.date.today()


class TestAcChargingSession(TestConfigureServer):
    @classmethod
    def setUpClass(self) -> None:
        super().setUpClass()
        print("charging session")
        self.CHARGER_URL = self.test_config["CHARGER_URL"]
        self.VEHICLE_URL_AC = self.test_config["VEHICLE_URL_AC"]
        self.CONNECT_AC = self.test_config["CONNECT_AC"]

    def setUp(self) -> None:
        if not self.check_charger_data(
            url_charger=self.CHARGER_SERVER_URL, key_word="ac_connect"
        ).json()["ac_connect"]:
            requests.post(f"{self.CONNECT_AC}{self.test_config['VEHICLE_CONNECT_AC']}")
        else:
            pass

    def test_reconfigure_parameter(self):
        print("SEND ENDPOINT TO CHANGE SOME VALUE IN SETTINGS")
        response_edit_param = requests.put(
            f"{self.VEHICLE_URL_AC}edit",
            json=self.test_config["VEHICLE_CHANGE_VALUE_AC"],
        )
        assert response_edit_param.status_code == 200
        print(response_edit_param.json())
        assert response_edit_param.json() == {"response": True, "error": None}

    def test_session_start(self):
        self.check_charger_data(url_charger=self.CHARGER_SERVER_URL, key_word="reload_settings_ac")
        requests.put(
            f"{self.VEHICLE_URL_AC}edit",
            json=self.test_config["VEHICLE_START_BATTERY_LEVEL_AC"],
        )
        print("CHECK SESSION FLOW AND PROPERLY COMPLETE")
        if self.test_config["START_SESSION_CUSTOM_PERCENT_AC"] is not None:
            start_session_url = f"{self.CHARGER_URL}{self.test_config['START_SESSION_AC']}_ac_{self.test_config['START_SESSION_CUSTOM_PERCENT_AC']}"
        else:
            start_session_url = f"{self.CHARGER_URL}{self.test_config['START_SESSION_AC']}_ac"
        response_session = requests.post(start_session_url)
        assert response_session.status_code == 200
        assert response_session.json() == {"response": True, "error": None}
        while True:
            if self.custom_timeout_ac() is True:
                assert (
                    self.check_charger_data(
                        url_charger=self.CHARGER_SERVER_URL, key_word="ac_finished"
                    ).json()["ac_finished"]
                    is True
                )
                break

    def test_vehicle_state_saved(self):
        self.test_session_start()
        print("CHECK SETTINGS AFTER SESSION SAVE PROPERLY!")
        response_check_setting = requests.get(
            f"{self.VEHICLE_URL_AC}{self.test_config['VEHICLE_TAKE_SPECIFIC_KEY_AC']}"
        )
        assert response_check_setting.status_code == 200
        assert response_check_setting.json() > self.test_config["VEHICLE_CHANGE_VALUE_AC"]["value"]

    def test_ac_charge_session_history_saved(self):
        self.test_session_start()
        print("CHECK CHARGING HISTORY IS CREATED AND SESSION IS SAVED CORRECTLY")
        session_history = self.check_vehicle_data(
            self.VEHICLE_SERVER_URL, key_word="ac_history"
        ).json()
        for key in self.test_config["VEHICLE_HISTORY_KEYS"]:
            assert key in session_history["AC"][0][f"{today}"]

    def test_ac_session_fillup(self):
        self.test_session_start()
        print("TEST AC SESSION FILL UP")
        session_history = self.check_vehicle_data(
            self.VEHICLE_SERVER_URL, key_word="ac_history"
        ).json()
        first_session_id = session_history["AC"][0][f"{today}"]["SESSION_ID"]
        start_session_url = f"{self.CHARGER_URL}{self.test_config['START_SESSION_AC']}_ac"
        response_session = requests.post(start_session_url)
        assert response_session.status_code == 200
        assert response_session.json() == {"response": True, "error": None}
        while True:
            if self.custom_timeout_ac() is True:
                assert (
                    self.check_charger_data(
                        url_charger=self.CHARGER_SERVER_URL, key_word="ac_finished"
                    ).json()["ac_finished"]
                    is True
                )
                break
        session_history = self.check_vehicle_data(
            self.VEHICLE_SERVER_URL, key_word="ac_history"
        ).json()
        fillup_session_id = session_history["AC"][0][f"{today}"]["SESSION_ID"]
        assert fillup_session_id == first_session_id

    def tearDown(self) -> None:
        if self.check_charger_data(
            url_charger=self.CHARGER_SERVER_URL, key_word="ac_connect"
        ).json()["ac_connect"]:
            requests.post(f"{self.VEHICLE_URL_AC}{self.test_config['VEHICLE_DISCONNECT_AC']}")
        else:
            pass
