from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from charger_vehicle_config_bridge import VehicleBridge as Vehicle
from charger_vehicle_config_bridge import ChargerBridge as Charger


class Structure(BaseModel):
	key: str
	value: str | int | float


router = APIRouter(
	prefix="/vehicle",
)


@router.post("/connect")
async def read_items():
	if Vehicle.connect["is_connected"]:
		return f"vehicle is already connected {Vehicle.connect}"
	Vehicle.connect["is_connected"] = True
	return f"Vehicle successful connected {Vehicle.connect}"


@router.post("/disconnect")
async def read_items():
	if Vehicle.connect["is_connected"]:
		Vehicle.connect["is_connected"] = False
		return f"Vehicle successful disconnected {Vehicle.connect}"
	return f"vehicle is disconnected {Vehicle.connect}"


@router.get("/all")
async def read_items():
	if Vehicle.connect["is_connected"]:
		return Vehicle.settings, Charger.settings
	raise HTTPException(status_code=404, detail="TO READ SETTINGS FIRST CONNECT VEHICLE!")


@router.get("/{item_id}")
async def read_item(item_id: str):
	if Vehicle.connect["is_connected"] and item_id in Vehicle.settings:
		return f"{item_id}={Vehicle.settings[item_id]}"
	elif Vehicle.connect["is_connected"] and item_id not in Vehicle.settings:
		raise HTTPException(status_code=404, detail="Setting not found in vehicle config!")
	raise HTTPException(status_code=404, detail="TO READ CONFIG FIRST CONNECT VEHICLE!")


@router.put("/")
async def update_item(struc: Structure):
	if Vehicle.connect["is_connected"]:
		if struc.key in Vehicle.settings:
			Vehicle.settings[struc.key] = struc.value
			return f"SUCCESSFULLY CHANGED VEHICLE PARAMETER: {struc.key}={Vehicle.settings[struc.key]}"
		raise HTTPException(status_code=404, detail="Setting not found in vehicle config!")
	raise HTTPException(status_code=404, detail="TO EDIT CONFIG FIRST CONNECT VEHICLE!")
