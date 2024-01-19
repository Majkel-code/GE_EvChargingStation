import config.charger_vehicle_config_bridge as Bridge
from config.charger_vehicle_config_bridge import VehicleBridge as Vehicle
from config.logging_system.logging_config import Logger
from fastapi import APIRouter, HTTPException, Request
from modules.battery.CHADEMO.chademo_battery import ChademoVehicleSpecification
from pydantic import BaseModel

chademo_vehicle_spec = ChademoVehicleSpecification


class Structure(BaseModel):
    key: str
    value: str | int | float


class Take(BaseModel):
    key: float


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
        raise HTTPException(
            status_code=404, detail="SETTING NOT FOUND IN VEHICLE SETTING"
        )
    raise HTTPException(status_code=404, detail=f"'{item_id}' CAN'T BE FIND!")


@router.put("/edit")
async def update_item(struc: Structure):
    if struc.key in Vehicle.settings_chademo:
        Vehicle.settings_chademo[struc.key] = struc.value
        if struc.key == "BATTERY_LEVEL":
            chademo_vehicle_spec_init = chademo_vehicle_spec()
            chademo_vehicle_spec_init.actual_battery_status_in_kwh = (
                chademo_vehicle_spec_init.current_battery_status_kwh()
            )
        logger.info(f"'{struc.key} SUCCESSFUL CHNAGED!'")
        return {"response": True, "error": None}
    return {"response": False, "error": f"{struc.key}' CAN'T BE FIND!"}


@router.patch("/kw_min")
async def take_kw_per_min(take: Take):
    try:
        chademo_vehicle_spec_init = chademo_vehicle_spec()
        chademo_vehicle_spec_init.actual_kw_per_min = take.key
        chademo_vehicle_spec_init.calculate_battery_increase()
    except Exception as e:
        logger.error(f"ERROR OCCURED: {e}")
