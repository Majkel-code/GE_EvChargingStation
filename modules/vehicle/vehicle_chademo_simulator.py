from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config.charger_vehicle_config_bridge import VehicleBridge as Vehicle
from config.charger_vehicle_config_bridge import ChargerBridge as Charger
import config.charger_vehicle_config_bridge as Bridge
from config.logging_system.logging_config import Logger


class Structure(BaseModel):
	key: str
	value: str | int | float


router = APIRouter(
	prefix="/vehicle_chademo",
)

logger = Logger.logger

@router.post("/connect")
async def read_items():
	if Vehicle._connected_chademo_:
		logger.warning(f"VEHICLE ACTUALLY CONNECTED: {Vehicle._connected_chademo_}")
		{"response": False, "error": "VEHICLE ACTUALLY CONNECTED!"}
	else:
		Bridge.connect_vehicle('CHADEMO')
		logger.info(f"VEHICLE SUCCESSFULY CONNECTED: {Vehicle._connected_chademo_}")
		return {"response": True, "error": None}


@router.post("/disconnect")
async def read_items():
	if Vehicle._connected_chademo_:
		Bridge.disconnect_vehicle("CHADEMO")
		logger.info(f"VEHICLE SUCCESSFULY DISCONNECTED: {Vehicle._connected_chademo_}")
		return {"response": True, "error": None}
	else:
		logger.warning(f"VEHICLE ACTUALLY IS DISCONNECTED: {Vehicle._connected_chademo_}")
		{"response": False, "error": "VEHICLE ACTUALLY IS DISCONNECTED!"}
	

@router.get("/all")
async def read_items():
	if Vehicle._connected_chademo_:
		return Vehicle.settings_chademo
	logger.error('TO READ SETTINGS FIRST CONNECT VEHICLE!')
	raise HTTPException(status_code=404, detail="REQUEST CAN'T BE FIND!")


@router.get("/{item_id}")
async def read_item(item_id: str):
	if Vehicle._connected_chademo_ and item_id in Vehicle.settings_chademo:
		logger.info(f"'{item_id}' FINDED IN VEHICLE!")
		return Vehicle.settings_chademo[item_id]
	elif Vehicle._connected_chademo_ and item_id not in Vehicle.settings_chademo:
		logger.error(f"'{item_id} CAN'T BE FINDED IN VEHICLE'")
		raise HTTPException(status_code=404, detail="SETTING NOT FOUND IN VEHICLE SETTING")
	raise HTTPException(status_code=404, detail=f"'{item_id}' CAN'T BE FIND!")

@router.put("/")
async def update_item(struc: Structure):
	if Vehicle._connected_chademo_:
		if struc.key in Vehicle.settings_chademo:
			Vehicle.settings_chademo[struc.key] = struc.value
			logger.info(f"'{struc.key} SUCCESSFUL CHNAGED!'")
			return {"response": True, "error": None}
		return {"response": False, "error": f"{struc.key}' CAN'T BE FIND!"}
	logger.error('TO READ SETTINGS FIRST CONNECT VEHICLE!')
	raise HTTPException(status_code=404, detail="REQUEST CAN'T BE FIND!")
