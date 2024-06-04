from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from veh_config.logging_system.logging_config import Logger
from veh_config.vehicle_config_bridge import VehicleBridge as Vehicle

from .vehicle_battery_bridge import VehicleBatteryBridge


class Structure(BaseModel):
    key: str
    value: str | int | float


class Take(BaseModel):
    key: float


class Complete(BaseModel):
    complete: bool


router = APIRouter(
    prefix="/vehicle_chademo",
)

logger = Logger.logger


@router.get("/all")
async def read_items():
    return Vehicle.settings_chademo


@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id in Vehicle.settings_chademo:
        logger.info(f"'{item_id}' FINDED IN VEHICLE!")
        return Vehicle.settings_chademo[item_id]
    elif item_id not in Vehicle.settings_chademo:
        logger.error(f"'{item_id} CAN'T BE FINDED IN VEHICLE'")
        raise HTTPException(status_code=404, detail="SETTING NOT FOUND IN VEHICLE SETTING")
    raise HTTPException(status_code=404, detail=f"'{item_id}' CAN'T BE FIND!")


@router.put("/edit")
async def update_item(struc: Structure):
    if struc.key in Vehicle.settings_chademo:
        if struc.key == "BATTERY_LEVEL":
            if struc.value > 100:
                return {
                    "response": False,
                    "error": "BATTERY LEVEL CAN'T BE >100%",
                }
            Vehicle.settings_chademo[struc.key] = struc.value
            VehicleBatteryBridge.reload_vehicle_specification(outlet="CHADEMO")
        Vehicle.settings_chademo[struc.key] = struc.value
        logger.info(f"'{struc.key} SUCCESSFUL CHNAGED!'")
        return {"response": True, "error": None}
    return {"response": False, "error": f"{struc.key}' CAN'T BE FIND!"}


@router.patch("/kw_min")
async def take_kw_per_min(take: Take):
    try:
        VehicleBatteryBridge.send_kw_to_battery(outlet="CHADEMO", kw_min=take.key)
    except Exception as e:
        logger.error(f"ERROR OCCURED: {e}")


@router.patch("/chademo_complete")
async def chademo_complete(complete: Complete):
    if complete.complete:
        VehicleBatteryBridge.perform_charge_saver("CHADEMO")
