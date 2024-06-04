from config.charger_vehicle_config_bridge import ChargerBridge as Charger
from config.charger_vehicle_config_bridge import VehicleBridge as Vehicle
from config.logging_system.logging_config import ServerLogger
from fastapi import APIRouter
from pydantic import BaseModel


class Structure(BaseModel):
    key: str
    value: str | int | float


router = APIRouter(
    prefix="/display_chademo",
)

server_logger = ServerLogger.logger_server


@router.get("/charging_chademo")
async def read_item():
    return {
        "BATTERY_LEVEL": Vehicle.settings_chademo["BATTERY_LEVEL"],
        "CHADEMO_KW_PER_MIN": Charger.settings["CHADEMO_ACTUAL_KW_PER_MIN"],
        "CHARGED_KW": Vehicle._charged_chademo_kw,
    }
