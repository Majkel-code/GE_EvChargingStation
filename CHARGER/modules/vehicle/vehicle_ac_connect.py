from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config.charger_vehicle_config_bridge import VehicleBridge as Vehicle
# from config.charger_vehicle_config_bridge import ChargerBridge as Charger
import config.charger_vehicle_config_bridge as Bridge
from config.logging_system.logging_config import Logger


class Structure(BaseModel):
    key: str
    value: str | int | float


router = APIRouter(
    prefix="/vehicle_ac",
)

logger = Logger.logger


@router.post("/connect")
async def read_items():
    if Vehicle._connected_ac_:
        logger.warning(f"VEHICLE ACTUALLY CONNECTED: {Vehicle._connected_ac_}")
        return {"response": False, "error": "VEHICLE ACTUALLY CONNECTED!"}
    else:
        handshake = Vehicle.connect_vehicle("AC")
        if handshake.ok:
            vehicle_specification = Vehicle.take_ac_vehicle_specification()
            if vehicle_specification.ok:
                logger.info(f"VEHICLE SUCCESSFULY CONNECTED AND SPECIFICATION READED")
                return {"response": True, "error": None}
            else:
                logger.warning(f"VEHICLE SUCCESSFULY CONNECTED BUT SPECIFICATION CAN'T BE TAKEN!")
                return {"response": True, "error":"VEHICLE SPECIFICATION CAN'T BE TAKEN"}
        else:
            logger.info(f"ERROR OCCURED WHEN TRYING CONNECT VEHICLE: {Vehicle._connected_ac_}")
            return {"response": False, "error": "FAIL VEHICLE CONNECT"}


@router.post("/disconnect")
async def read_items():
    if Vehicle._connected_ac_:
        disconnect = Vehicle.disconnect_vehicle("AC")
        if disconnect.ok:
            logger.info(f"VEHICLE SUCCESSFULY DISCONNECTED: {Vehicle._connected_ac_}")
            return {"response": True, "error": None}
    else:
        logger.warning(f"VEHICLE ACTUALLY IS DISCONNECTED: {Vehicle._connected_ac_}")
        return {"response": False, "error": "VEHICLE ACTUALLY IS DISCONNECTED!"}
    