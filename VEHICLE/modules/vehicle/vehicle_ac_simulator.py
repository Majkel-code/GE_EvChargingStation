from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config.charger_vehicle_config_bridge import VehicleBridge as Vehicle
import config.charger_vehicle_config_bridge as Bridge
from config.logging_system.logging_config import Logger
from .vehicle_battery_bridge import VehicleBatteryBridge


class Structure(BaseModel):
    key: str
    value: str | int | float


class Take(BaseModel):
    key: float


router = APIRouter(
    prefix="/vehicle_ac",
)

logger = Logger.logger


@router.get("/all")
async def read_items():
    return Vehicle.settings_ac


@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id in Vehicle.settings_ac:
        logger.info(f"'{item_id}' FINDED IN VEHICLE!")
        return Vehicle.settings_ac[item_id]
    elif item_id not in Vehicle.settings_ac:
        logger.error(f"'{item_id} CAN'T BE FINDED IN VEHICLE'")
        raise HTTPException(status_code=404, detail="SETTING NOT FOUND IN VEHICLE SETTING")
    raise HTTPException(status_code=404, detail=f"'{item_id}' CAN'T BE FIND!")


@router.put("/edit")
async def update_item(struc: Structure):
    if struc.key in Vehicle.settings_ac:
        if struc.key == "BATTERY_LEVEL":
            if struc.value > 100:
                return {"response": False, "error": "BATTERY LEVEL CAN'T BE >100%"}
            Vehicle.settings_ac[struc.key] = struc.value
            VehicleBatteryBridge.reload_vehicle_specification(outlet="AC")
        Vehicle.settings_ac[struc.key] = struc.value
        logger.info(f"'{struc.key} SUCCESSFUL CHNAGED!'")
        return {"response": True, "error": None}
    return {"response": False, "error": f"{struc.key}' CAN'T BE FIND!"}


@router.patch("/kw_min")
async def take_kw_per_min(take: Take):
    try:
        VehicleBatteryBridge.send_kw_to_battery(outlet="AC", kw_min=take.key)
    except Exception as e:
        logger.error(f"ERROR OCCURED: {e}")
