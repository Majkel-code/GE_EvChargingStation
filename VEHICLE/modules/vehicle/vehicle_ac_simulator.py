from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from config.charger_vehicle_config_bridge import VehicleBridge as Vehicle
import config.charger_vehicle_config_bridge as Bridge
from config.logging_system.logging_config import Logger
import json


class Structure(BaseModel):
    key: str
    value: str | int | float


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
        Vehicle.settings_ac[struc.key] = struc.value
        logger.info(f"'{struc.key} SUCCESSFUL CHNAGED!'")
        return {"response": True, "error": None}
    # raise HTTPException(status_code=404, detail="REQUEST CAN'T BE FIND!")
    return {"response": False, "error": f"{struc.key}' CAN'T BE FIND!"}


@router.patch("/spec")
async def read_save_spec_from_charger(request: Request):
    r = request
    if len(Vehicle.settings_ac) == len(await r.json()):
        Vehicle.settings_ac = await r.json()
    else:
        logger.error(f"ERROR OCCURED WHEN TAKING CHARGING INFO FROM CHARGER")
