from config.logging_system.logging_config import Logger
import uvicorn
import yaml
from fastapi import FastAPI
import modules.charger.charger as charger
import config.charger_vehicle_config_bridge as charger_vehicle_config_bridge
from config.charger_vehicle_config_bridge import __IsServerAlive__ as _is_server_alive
import modules.vehicle.vehicle_simulator as vehicle_simulator

logger= Logger.logger
app = FastAPI()
app.include_router(charger.router)
app.include_router(vehicle_simulator.router)


class Server:
	def start():
		if not _is_server_alive._is_alive_:
			try:
				server = InitialiseServer
				_is_server_alive._is_alive_ = True
				InitialiseServer.server.run()
				logger.info("SERVER CLOSED SUCCESSFUL!")
				_is_server_alive._is_alive_ = False
			except Exception as e:
				logger.critical("UNABLE TO ESTABLISH SERVER!")
				return {"response": False, "error": e}
		return _is_server_alive._is_alive_


class InitialiseServer:
	try:
		config_charger = charger_vehicle_config_bridge.ChargerBridge()
		config_vehicle = charger_vehicle_config_bridge.VehicleBridge()
		with open("config/config_files/server_config.yaml", "r+") as f:
			server_config = yaml.safe_load(f)
		config = uvicorn.Config(app=server_config["SERVER_APP"],
								port=server_config["PORT"],
								log_config=None,
								log_level=server_config["LOG_LEVEL"],
								host=server_config["HOST_IP"],
								reload=server_config["RELOAD"])
		server = uvicorn.Server(config)
	except Exception as e:
		logger.error(e)


if __name__ == "__main__":
	start = Server.start()
