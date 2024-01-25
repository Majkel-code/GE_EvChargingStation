import requests

from tests.test_configuration import TestConfigureServer


class TestServer(TestConfigureServer):
    @classmethod
    def setUpClass(self) -> None:
        super().setUpClass()
        print("server test")

    def test_charger_is_alive(self):
        print("TEST SERVER IS ALIVE!")
        request = requests.get(f'{self.CHARGER_SERVER_URL}{self.test_config["SERVER_IS_ALIVE"]}')
        assert request.status_code == 200
        assert request.json() == {"is_alive": True, "error": None}

    def test_vehicle_is_alive(self):
        print("TEST SERVER IS ALIVE!")
        request = requests.get(f'{self.VEHICLE_SERVER_URL}{self.test_config["SERVER_IS_ALIVE"]}')
        assert request.status_code == 200
        assert request.json() == {"is_alive": True, "error": None}

    @classmethod
    def tearDownClass(self) -> None:
        super().tearDownClass()
