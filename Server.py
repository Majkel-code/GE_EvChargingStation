import uvicorn
import yaml
from fastapi import FastAPI
import charger
import charger_vehicle_config
import vehicle_simulator


app = FastAPI()
app.include_router(charger.router)
app.include_router(vehicle_simulator.router)


def server():
	config_charger = charger_vehicle_config.ChargerBridge()
	config_vehicle = charger_vehicle_config.VehicleBridge()
	with open("server_config.yaml", "r+") as f:
		server_config = yaml.safe_load(f)
	config = uvicorn.Config(server_config["SERVER_APP"],
							port=server_config["PORT"],
							log_level=server_config["LOG_LEVEL"],
							host=server_config["HOST_IP"],
							reload=server_config["RELOAD"])
	server = uvicorn.Server(config)
	server.run()


if __name__ == "__main__":
	server()
