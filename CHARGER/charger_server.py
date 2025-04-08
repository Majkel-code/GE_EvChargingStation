from pathlib import Path

import config.charger_vehicle_config_bridge as charger_vehicle_config_bridge
import modules.charger.charger as charger
import modules.vehicle.vehicle_ac_connect as vehicle_ac_connect
import modules.vehicle.vehicle_chademo_connect as vehicle_chademo_connect
import uvicorn
import yaml
from config.charger_vehicle_config_bridge import IsServerAlive as _main_server
from config.config_reader.generate_auth_key import AuthorizationSystem
from config.logging_system.logging_config import ServerLogger
from fastapi import FastAPI, Request
from modules.display import display_ac, display_chademo

server_logger = ServerLogger.logger_server


class InitialiseServer:
    def __init__(self) -> None:
        try:
            self.app = FastAPI()
            self.app.include_router(charger.router)
            self.app.include_router(vehicle_ac_connect.router)
            self.app.include_router(vehicle_chademo_connect.router)
            self.app.include_router(display_ac.router)
            self.app.include_router(display_chademo.router)
            self.server = uvicorn.Server
            charger_vehicle_config_bridge.ChargerBridge()
            current_path = Path(__file__).absolute().parent
            config_path = f"{current_path}/config/config_files"
            with open(
                f"{config_path}/charger_server_config.yaml",
                "r+",
            ) as f:
                server_config = yaml.safe_load(f)
            self.auth = AuthorizationSystem(f"{Path(__file__).absolute().parents[1]}/AUTHORIZATION_KEY/host_key.txt")
            self.config = uvicorn.Config(
                app=self.app,
                port=server_config["PORT"],
                log_config=None,
                log_level=server_config["LOG_LEVEL_SERVER"],
                host=server_config["HOST_IP"],
                reload=server_config["RELOAD"],
            )

            @self.app.get("/{name}")
            async def check(name: str, request: Request):
                data_to_return = None
                key = request.headers.get("authorization")
                if self.auth.read_local_key() == key:
                    if name == "is_alive":
                        data_to_return = _main_server.check_server_is_alive()

                    elif name == "ac_connect":
                        data_to_return = (
                            charger_vehicle_config_bridge.VehicleBridge.check_connection("AC")
                        )

                    elif name == "chademo_connect":
                        data_to_return = (
                            charger_vehicle_config_bridge.VehicleBridge.check_connection("CHADEMO")
                        )

                    elif name == "ac_charging_ongoing":
                        data_to_return = charger_vehicle_config_bridge.ChargerBridge.energy_ongoing(
                            "AC"
                        )

                    elif name == "chademo_charging_ongoing":
                        data_to_return = charger_vehicle_config_bridge.ChargerBridge.energy_ongoing(
                            "CHADEMO"
                        )

                    elif name == "ac_finished":
                        data_to_return = (
                            charger_vehicle_config_bridge.ChargerBridge.session_finished("AC")
                        )

                    elif name == "chademo_finished":
                        data_to_return = (
                            charger_vehicle_config_bridge.ChargerBridge.session_finished("CHADEMO")
                        )

                    elif name == "reload_settings_ac":
                        data_to_return = (
                            charger_vehicle_config_bridge.VehicleBridge.take_ac_vehicle_specification().ok
                        )

                    elif name == "reload_settings_chademo":
                        data_to_return = (
                            charger_vehicle_config_bridge.VehicleBridge.take_chademo_vehicle_specification().ok
                        )
                else:
                    server_logger.error("UNABLE TO AUTHORIZE REQUEST!")
                    return {
                        "response": "NOK",
                        "error": "UNABLE TO AUTHORIZE REQUEST!",
                        "data": None,
                    }
                return {
                        "response": "OK",
                        "error": None,
                        "data": {f"{name}": data_to_return},
                    }
                # return {f"{name}": data_to_return}

        except Exception as e:
            server_logger.error(e)


class Server(InitialiseServer):
    def start(self):
        if not _main_server._is_alive_:
            try:
                _main_server._is_alive_ = True
                self.server = self.server(self.config)
                self.server.run()
                server_logger.info("SERVER CLOSED SUCCESSFUL!")
                _main_server._is_alive_ = False
            except Exception as e:
                server_logger.critical(f"UNABLE TO ESTABLISH SERVER! {e}")


if __name__ == "__main__":
    start = Server()
    start.start()
