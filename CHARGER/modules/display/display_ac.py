from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config.charger_vehicle_config_bridge import VehicleBridge as Vehicle
# from config.charger_vehicle_config_bridge import ChargerBridge as Charger
import config.charger_vehicle_config_bridge as Bridge
from config.logging_system.logging_config import ServerLogger


class Structure(BaseModel):
    key: str
    value: str | int | float


router = APIRouter(
    prefix="/display_ac",
)

server_logger = ServerLogger.logger_server

@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id in Vehicle.settings_ac:
        server_logger.info(f"'{item_id}' FINDED IN VEHICLE!")
        return Vehicle.settings_ac[item_id]
    elif item_id not in Vehicle.settings_ac:
        server_logger.error(f"'{item_id} CAN'T BE FINDED IN VEHICLE'")
        raise HTTPException(status_code=404, detail="SETTING NOT FOUND IN VEHICLE SETTING")
    raise HTTPException(status_code=404, detail=f"'{item_id}' CAN'T BE FIND!")