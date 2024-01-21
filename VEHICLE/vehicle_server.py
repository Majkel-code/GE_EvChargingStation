from pathlib import Path

import modules.vehicle.handshakes.ac_handshake as ac_handshake
import modules.vehicle.handshakes.chademo_handshake as chademo_handshake
import modules.vehicle.vehicle_ac_simulator as vehicle_ac_simulator
import modules.vehicle.vehicle_chademo_simulator as vehicle_chademo_simulator
import uvicorn
import yaml
from config.charger_vehicle_config_bridge import IsServerAlive as _main_server
from config.charger_vehicle_config_bridge import VehicleBridge
from config.logging_system.logging_config import Logger
from fastapi import FastAPI
from modules.battery.AC.ac_battery import AcVehicleSpecification
from modules.battery.CHADEMO.chademo_battery import ChademoVehicleSpecification

logger = Logger.logger


class InitialiseServer:
    def __init__(self) -> None:
        try:
            self.app = FastAPI()
            VehicleBridge.ac_load_configuration()
            VehicleBridge.chademo_load_configuration()
            self.app.include_router(vehicle_ac_simulator.router)
            self.app.include_router(vehicle_chademo_simulator.router)
            self.app.include_router(ac_handshake.router)
            self.app.include_router(chademo_handshake.router)
            AcVehicleSpecification()
            ChademoVehicleSpecification()
            self.server = uvicorn.Server
            current_path = Path(__file__).absolute().parent
            with open(
                f"{current_path}/config/config_files/vehicle_server_config.yaml",
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

        except Exception as e:
            logger.error(e)


class Server(InitialiseServer):
    def start(self):
        if not _main_server._is_alive_:
            try:
                _main_server._is_alive_ = True
                self.server = self.server(self.config)
                self.server.run()
                logger.info("SERVER CLOSED SUCCESSFUL!")
                _main_server._is_alive_ = False
            except Exception as e:
                _main_server._is_alive_ = False
                logger.critical(f"UNABLE TO ESTABLISH SERVER! {e}")


if __name__ == "__main__":
    start = Server()
    start.start()
