from threading import Thread
from fastapi import APIRouter, HTTPException
import charge_simulation
from pydantic import BaseModel
from configs.charger_vehicle_config_bridge import VehicleBridge as Vehicle
from configs.charger_vehicle_config_bridge import ChargerBridge as Charger


class Structure(BaseModel):
	key: str
	value: str | int | float


router = APIRouter(
	prefix="/charger"
)


@router.get("/all")
async def read_items():
	if Vehicle.connect["is_connected"]:
		return Charger.settings, Vehicle.settings
	return Charger.settings


@router.get("/{item_id}")
async def read_item(item_id: str):
	if item_id not in Charger.settings:
		raise HTTPException(status_code=404, detail="Setting not found in charger config")
	return Charger.settings[item_id]


@router.post("/start")
async def read_items():
	if Vehicle.connect["is_connected"]:
		initialize_charge_simulation = charge_simulation.ChargeSimulation()
		thread = Thread(target=initialize_charge_simulation.prepare_charging)
		thread.start()
		return "CHARGING STARTED!"
	raise HTTPException(status_code=404, detail="TO START SESSION FIRST CONNECT VEHICLE!")


# @router.put("/")
# async def update_item(key: str, value: str | int | float):
# 	default_settings[key] = value
# 	return f"SUCCESSFULLY CHENGED PARAMETER: {key}={default_settings[key]}"

@router.put("/")
async def update_item(struc: Structure):
	Charger.settings[struc.key] = struc.value
	return f"SUCCESSFULLY CHENGED CHARGER PARAMETER: {struc.key}={Charger.settings[struc.key]}"
