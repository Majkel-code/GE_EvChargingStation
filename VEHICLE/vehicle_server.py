from pathlib import Path

import uvicorn
import veh_modules.vehicle.handshakes.ac_handshake as ac_handshake
import veh_modules.vehicle.handshakes.chademo_handshake as chademo_handshake
import veh_modules.vehicle.vehicle_ac_simulator as vehicle_ac_simulator
import veh_modules.vehicle.vehicle_chademo_simulator as vehicle_chademo_simulator
import yaml
from fastapi import FastAPI
from veh_config.logging_system.logging_config import Logger
from veh_config.vehicle_config_bridge import IsServerAlive as _main_server
from veh_config.vehicle_config_bridge import VehicleBridge
from veh_modules.battery.AC.ac_battery import AcVehicleSpecification
from veh_modules.battery.CHADEMO.chademo_battery import ChademoVehicleSpecification
from veh_modules.vehicle.vehicle_battery_bridge import VehicleBatteryBridge 

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
            VehicleBatteryBridge.ac_vehicle_spec = AcVehicleSpecification()
            VehicleBatteryBridge.chademo_vehicle_spec = ChademoVehicleSpecification()
            self.server = uvicorn.Server
            current_path = Path(__file__).absolute().parent
            with open(
                f"{current_path}/veh_config/config_files/vehicle_server_config.yaml",
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

            @self.app.get("/{name}")
            async def veh_check(name: str):
                data_to_return = None

                if name == "is_alive":
                    data_to_return = _main_server.check_server_is_alive()

                if name == "reload_ac":
                    VehicleBridge.ac_load_configuration()
                    AcVehicleSpecification()
                    data_to_return = True

                if name == "reload_chademo":
                    VehicleBridge.chademo_load_configuration()
                    ChademoVehicleSpecification()
                    data_to_return = True

                if name == "ac_history":
                    return AcVehicleSpecification.read_charge_history(AcVehicleSpecification, outlet="AC")
                if name == "chademo_history":
                    return ChademoVehicleSpecification.read_charge_history(ChademoVehicleSpecification, outlet="CHADEMO")

                return {f"{name}": data_to_return}

        except Exception as e:
            logger.error(e)


class Server(InitialiseServer):
    def start(self):
        if not _main_server._is_alive_:
            try:
                _main_server._is_alive_ = True
                self.server = self.server(self.config)
                self.server.run()
                VehicleBatteryBridge.save_after_server_shutdown()
                logger.info("SERVER CLOSED SUCCESSFUL!")
                _main_server._is_alive_ = False
            except Exception as e:
                _main_server._is_alive_ = False
                logger.critical(f"UNABLE TO ESTABLISH SERVER! {e}")


if __name__ == "__main__":
    start = Server()
    start.start()
