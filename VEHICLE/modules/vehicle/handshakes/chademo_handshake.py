from config.charger_vehicle_config_bridge import VehicleBridge as Vehicle
from config.logging_system.logging_config import Logger
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


class Structure_connect(BaseModel):
    id: str
    # value: str | int | float


class Structure_disconnect(BaseModel):
    id: str
    end_connection: bool


router = APIRouter(
    prefix="/handshake_chademo",
)

logger = Logger.logger


@router.put("/connect")
async def take_connect_info(struc: Structure_connect):
    if struc.id is not None:
        try:
            Vehicle.settings_chademo["SESSION_ID"] = struc.id

        except Exception as e:
            logger.error(e)
            return {"response": False, "error": e}


@router.put("/disconnect")
async def take_disconnect_request(struc: Structure_disconnect):
    if (
        struc.id == Vehicle.settings_chademo["SESSION_ID"]
        and struc.end_connection
    ):
        Vehicle.settings_chademo["SESSION_ID"] = None
