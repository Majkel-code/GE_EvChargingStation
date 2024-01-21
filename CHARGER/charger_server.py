from pathlib import Path

import config.charger_vehicle_config_bridge as charger_vehicle_config_bridge
import modules.charger.charger as charger
import modules.vehicle.vehicle_ac_connect as vehicle_ac_connect
import modules.vehicle.vehicle_chademo_connect as vehicle_chademo_connect
import uvicorn
import yaml
from config.charger_vehicle_config_bridge import IsServerAlive as _main_server
from config.logging_system.logging_config import ServerLogger
from fastapi import FastAPI
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
            self.config = uvicorn.Config(
                app=self.app,
                port=server_config["PORT"],
                log_config=None,
                log_level=server_config["LOG_LEVEL_SERVER"],
                host=server_config["HOST_IP"],
                reload=server_config["RELOAD"],
            )

            @self.app.get("/is_alive")
            async def alive():
                return {
                    "is_alive": _main_server.check_server_is_alive(),
                    "error": None,
                }

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
