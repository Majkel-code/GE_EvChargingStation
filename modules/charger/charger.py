from threading import Thread
from fastapi import APIRouter, HTTPException
import simulations.charge_simulation as charge_simulation
from pydantic import BaseModel
from config.charger_vehicle_config_bridge import VehicleBridge as Vehicle
from config.charger_vehicle_config_bridge import ChargerBridge as Charger
import config.charger_vehicle_config_bridge as charger_vehicle_config_bridge
from config.logging_system.logging_config import Logger


class Structure(BaseModel):
	key: str
	value: str | int | float


router = APIRouter(
	prefix="/charger"
)

logger = Logger.logger
@router.get("/live")
async def read_items():
	return charger_vehicle_config_bridge.__IsServerAlive__._is_alive_

@router.get("/all")
async def read_items():
	if Vehicle.connect["is_connected"]:
		logger.info("PROPERLY READED SETTINGS")
		return Charger.settings, Vehicle.settings
	logger.info("PROPERLY READED SETTINGS")
	return Charger.settings


@router.get("/{item_id}")
async def read_item(item_id: str):
	if item_id not in Charger.settings:
		logger.error(f"'{item_id}' CAN'T BE FINDED IN CHARGER!")
		raise HTTPException(status_code=404, detail="REQUEST CAN'T BE FIND!")
	return Charger.settings[item_id]


@router.post("/start")
async def read_items():
	if Vehicle.connect["is_connected"]:
		try:
			initialize_charge_simulation = charge_simulation.ChargeSimulation()
			thread = Thread(target=initialize_charge_simulation.prepare_charging)
			thread.start()
			logger.info("SESSION INITIALIZE...")
			return {"response": True, "error": None}
		except Exception as e:
			logger.error(f"UNABLE TO INITIALIZE SESSION! {e}")
			return {"response": False, "error": e}
	logger.warning("TO START SESSION FIRST CONNECT VEHICLE!")
	raise HTTPException(status_code=404, detail="REQUEST CAN'T BE FIND!")


@router.put("/")
async def update_item(struc: Structure):
	if struc.key in Charger.settings:
		try:
			Charger.settings[struc.key] = struc.value
			logger.info(F"{struc.key}={struc.value} SETTING PROLERLY CHANGED...")
			return {"response": True, "error": None}
		except Exception as e:
			logger.error("UNABE TO CHANGE SETTING!")
			return {"response": False, "error": e}
	logger.error(f"'{struc.key}' NOT EXIST IN CHARGER SETTINGS!")
	raise HTTPException(status_code=404, detail="REQUEST CAN'T BE FIND!")
