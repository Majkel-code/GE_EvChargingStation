from config.charger_vehicle_config_bridge import VehicleBridge as Vehicle
from config.logging_system.logging_config import ServerLogger
from fastapi import APIRouter
from pydantic import BaseModel


class Structure(BaseModel):
    key: str
    value: str | int | float


router = APIRouter(
    prefix="/vehicle_ac",
)

server_logger = ServerLogger.logger_server


@router.post("/connect")
async def read_items():
    if Vehicle._connected_ac_:
        server_logger.warning(f"VEHICLE ACTUALLY CONNECTED: {Vehicle._connected_ac_}")
        return {"response": False, "error": "VEHICLE ACTUALLY CONNECTED!"}
    else:
        handshake = Vehicle.connect_vehicle("AC")
        if handshake["handshake_ac"]:
            vehicle_specification = Vehicle.take_ac_vehicle_specification()
            if vehicle_specification.ok:
                server_logger.info("VEHICLE SUCCESSFULY CONNECTED AND SPECIFICATION READED")
                return {"response": True, "error": None}
            else:
                server_logger.warning(
                    "VEHICLE SUCCESSFULY CONNECTED BUT SPECIFICATION CAN'T BE TAKEN!"
                )
                return {
                    "response": True,
                    "error": "VEHICLE SPECIFICATION CAN'T BE TAKEN",
                }
        else:
            server_logger.info(
                f"ERROR OCCURED WHEN TRYING CONNECT VEHICLE: {Vehicle._connected_ac_}"
            )
            return {"response": False, "error": "FAIL VEHICLE CONNECT"}


@router.post("/disconnect")
async def disconnect():
    if Vehicle._connected_ac_:
        disconnect = Vehicle.disconnect_vehicle("AC")
        if disconnect["disconnect_ac"]:
            server_logger.info(f"VEHICLE SUCCESSFULY DISCONNECTED: {Vehicle._connected_ac_}")
            return {"response": True, "error": None}
    else:
        server_logger.warning(f"VEHICLE ACTUALLY IS DISCONNECTED: {Vehicle._connected_ac_}")
        return {
            "response": False,
            "error": "VEHICLE ACTUALLY IS DISCONNECTED!",
        }
