from fastapi import APIRouter
from pydantic import BaseModel
from veh_config.logging_system.logging_config import Logger
from veh_config.vehicle_config_bridge import VehicleBridge as Vehicle
from veh_modules.vehicle.vehicle_battery_bridge import VehicleBatteryBridge
from veh_modules.battery.CHADEMO.chademo_battery import ChademoVehicleSpecification


class Structure_connect(BaseModel):
    id: str


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
    if struc.id == Vehicle.settings_chademo["SESSION_ID"] and struc.end_connection:
        try:
            VehicleBatteryBridge.perform_charge_saver("CHADEMO")
            Vehicle.chademo_load_configuration()
            VehicleBatteryBridge.chademo_vehicle_spec = ChademoVehicleSpecification()
        except Exception as e:
            logger.error(e)
