import requests
from config import charger_vehicle_config_bridge

from tests.test_server import TestConfigureServer


class TestAcVehicleEndpoints(TestConfigureServer):
    @classmethod
    def setUpClass(self) -> None:
        super().setUpClass()
        self.CHARGER_URL = self.test_config["CHARGER_URL"]
        self.VEHICLE_URL_AC = self.test_config["VEHICLE_URL_AC"]
        self.VEHICLE_EVERY_SETTING = self.test_config["VEHICLE_CHECK_EVERY_SETTINGS_AC"]
        self.VEHICLE_URL_CHADEMO = self.test_config["VEHICLE_URL_CHADEMO"]
        self.VEHICLE_EVERY_SETTING = self.test_config["VEHICLE_CHECK_EVERY_SETTINGS_CHADEMO"]
        print("vehicle")

    def setUp(self) -> None:
        if not charger_vehicle_config_bridge.VehicleBridge._connected_ac_:
            requests.post(f"{self.VEHICLE_URL_AC}{self.test_config['VEHICLE_CONNECT_AC']}")
        else:
            pass
        if not charger_vehicle_config_bridge.VehicleBridge._connected_chademo_:
            requests.post(
                f"{self.VEHICLE_URL_CHADEMO}{self.test_config['VEHICLE_CONNECT_CHADEMO']}"
            )
        else:
            pass

    def test_reconfigure_parameter(self):
        print("SEND ENDPOINT TO CHANGE SOME VALUE IN SETTINGS")
        # chademo
        response_edit_param_chademo = requests.put(
            self.VEHICLE_URL_CHADEMO,
            json=self.test_config["VEHICLE_CHANGE_VALUE_CHADEMO"],
        )
        assert response_edit_param_chademo.status_code == 200
        print(response_edit_param_chademo.json())
        assert response_edit_param_chademo.json() == {
            "response": True,
            "error": None,
        }
        # ac
        response_edit_param_ac = requests.put(
            self.VEHICLE_URL_AC,
            json=self.test_config["VEHICLE_CHANGE_VALUE_AC"],
        )
        assert response_edit_param_ac.status_code == 200
        print(response_edit_param_ac.json())
        assert response_edit_param_ac.json() == {
            "response": True,
            "error": None,
        }

    def test_session_start(self):
        self.read_vehicle_chademo_settings()
        requests.put(
            self.VEHICLE_URL_CHADEMO,
            json=self.test_config["VEHICLE_START_BATTERY_LEVEL_CHADEMO"],
        )
        requests.put(
            self.VEHICLE_URL_AC,
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
            if self.custom_timeout_chademo() and self.custom_timeout_ac():
                assert (
                    charger_vehicle_config_bridge.ChargerBridge._charging_finished_chademo_ is True
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
        if charger_vehicle_config_bridge.VehicleBridge._connected_chademo_:
            requests.post(
                f"{self.VEHICLE_URL_CHADEMO}{self.test_config['VEHICLE_DISCONNECT_CHADEMO']}"
            )
        else:
            pass
        if charger_vehicle_config_bridge.VehicleBridge._connected_ac_:
            requests.post(f"{self.VEHICLE_URL_AC}{self.test_config['VEHICLE_CONNECT_AC']}")
        else:
            pass
