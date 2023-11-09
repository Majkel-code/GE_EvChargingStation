from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config.charger_vehicle_config_bridge import VehicleBridge as Vehicle
from config.charger_vehicle_config_bridge import ChargerBridge as Charger
from config.logging_system.logging_config import Logger


class Structure(BaseModel):
	key: str
	value: str | int | float


router = APIRouter(
	prefix="/vehicle",
)

logger = Logger.logger

@router.post("/connect")
async def read_items():
	if Vehicle.connect["is_connected"]:
		logger.warning(f"VEHICLE ACTUALLY CONNECTED: {Vehicle.connect}")
		{"response": False, "error": "VEHICLE ACTUALLY CONNECTED!"}
	Vehicle.connect["is_connected"] = True
	logger.info(f"VEHICLE SUCCESSFULY CONNECTED: {Vehicle.connect}")
	return {"response": True, "error": None}


@router.post("/disconnect")
async def read_items():
	if Vehicle.connect["is_connected"]:
		Vehicle.connect["is_connected"] = False
		return {"response": True, "error": None}
		logger.info(f"VEHICLE SUCCESSFULY DISCONNECTED: {Vehicle.connect}")
	logger.warning(f"VEHICLE ACTUALLY DISCONNECTED: {Vehicle.connect}")
	{"response": False, "error": "VEHICLE ACTUALLY DISCONNECTED!"}


@router.get("/all")
async def read_items():
	if Vehicle.connect["is_connected"]:
		return Vehicle.settings, Charger.settings
	logger.error('TO READ SETTINGS FIRST CONNECT VEHICLE!')
	raise HTTPException(status_code=404, detail="REQUEST CAN'T BE FIND!")


@router.get("/{item_id}")
async def read_item(item_id: str):
	if Vehicle.connect["is_connected"] and item_id in Vehicle.settings:
		logger.info(f"'{item_id}' FINDED IN VEHICLE!")
		return f"{item_id}={Vehicle.settings[item_id]}"
	elif Vehicle.connect["is_connected"] and item_id not in Vehicle.settings:
		logger.error(f"'{item_id} CAN'T BE FINDED IN VEHICLE'")
		raise HTTPException(status_code=404, detail="SETTING NOT FOUND IN VEHICLE SETTING")
	raise HTTPException(status_code=404, detail=f"'{item_id}' CAN'T BE FIND!")


@router.put("/")
async def update_item(struc: Structure):
	if Vehicle.connect["is_connected"]:
		if struc.key in Vehicle.settings:
			Vehicle.settings[struc.key] = struc.value
			logger.info(f"'{struc.key} SUCCESSFUL CHNAGED!'")
			return f"{struc.key}={Vehicle.settings[struc.key]}"
		raise HTTPException(status_code=404, detail=F"{struc.key}' CAN'T BE FIND!")
	logger.error('TO READ SETTINGS FIRST CONNECT VEHICLE!')
	raise HTTPException(status_code=404, detail="REQUEST CAN'T BE FIND!")
