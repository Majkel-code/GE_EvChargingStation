from config.logging_system.logging_config import Logger
import uvicorn
import yaml
from fastapi import FastAPI
import modules.charger.charger as charger
import config.charger_vehicle_config_bridge as charger_vehicle_config_bridge
from config.charger_vehicle_config_bridge import __IsServerAlive__ as _main_server
import modules.vehicle.vehicle_simulator as vehicle_simulator

logger = Logger.logger


class InitialiseServer:
	def __init__(self) -> None:
		try:
			self.app = FastAPI()
			self.app.include_router(charger.router)
			self.app.include_router(vehicle_simulator.router)
			self.server = uvicorn.Server
			config_charger = charger_vehicle_config_bridge.ChargerBridge()
			config_vehicle = charger_vehicle_config_bridge.VehicleBridge()
			with open("config/config_files/server_config.yaml", "r+") as f:
				server_config = yaml.safe_load(f)
			self.config = uvicorn.Config(app=self.app,
									port=server_config["PORT"],
									log_config=None,
									log_level=server_config["LOG_LEVEL_SERVER"],
									host=server_config["HOST_IP"],
									reload=server_config["RELOAD"])
		except Exception as e:
			logger.error(e)

class Server(InitialiseServer):
	def __init__(self) -> None:
		super().__init__()
	def start(self):
		if not _main_server._is_alive_:
			try:
				_main_server._is_alive_ = True
				self.server = self.server(self.config)
				self.server.run()
				logger.info("SERVER CLOSED SUCCESSFUL!")
				_main_server._is_alive_ = False
			except Exception as e:
				logger.critical("UNABLE TO ESTABLISH SERVER!")
				return {"response": False, "error": e}
		return _main_server._is_alive_

if __name__ == "__main__":
	start = Server()
	start.start()
