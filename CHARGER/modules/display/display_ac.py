from config.charger_vehicle_config_bridge import ChargerBridge as Charger
from config.charger_vehicle_config_bridge import VehicleBridge as Vehicle
from config.logging_system.logging_config import ServerLogger
from fastapi import APIRouter
from pydantic import BaseModel


class Structure(BaseModel):
    key: str
    value: str | int | float


router = APIRouter(
    prefix="/display_ac",
)

server_logger = ServerLogger.logger_server


@router.get("/charging_ac")
async def read_item():
    return {
        "BATTERY_LEVEL": Vehicle.settings_ac["BATTERY_LEVEL"],
        "AC_KW_PER_MIN": Charger.settings["AC_ACTUAL_KW_PER_MIN"],
        "CHARGED_KW": Vehicle._charged_ac_kw,
    }
