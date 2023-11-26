from logging_config import Logger
import uvicorn
import yaml
from fastapi import FastAPI
import charger
import charger_vehicle_config_bridge
import vehicle_simulator


logger = Logger.logger
app = FastAPI()
app.include_router(charger.router)
app.include_router(vehicle_simulator.router)


class ChargerServer:
	try:
		config_charger = charger_vehicle_config_bridge.ChargerBridge()
		config_vehicle = charger_vehicle_config_bridge.VehicleBridge()
		with open("server_config.yaml", "r+") as f:
			server_config = yaml.safe_load(f)
		config = uvicorn.Config(server_config["SERVER_APP"],
								port=server_config["PORT"],
								log_config=None,
								log_level=server_config["LOG_LEVEL"],
								host=server_config["HOST_IP"],
								reload=server_config["RELOAD"])
		server = uvicorn.Server(config)
	except Exception as e:
		logger.error(e)


if __name__ == "__main__":
	prepare = ChargerServer
	prepare.server.run()
	logger.info("SERVER CLOSED SUCCESSFUL!")
