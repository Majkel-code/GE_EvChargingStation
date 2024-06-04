import time
from threading import Thread

from config.charger_vehicle_config_bridge import ChargerBridge as Charger
from config.charger_vehicle_config_bridge import VehicleBridge as Vehicle
from config.logging_system.logging_config import (
    ACChargeSessionLogger,
    CHADEMOChargeSessionLogger,
    ServerLogger,
)
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from simulations import ac_charge_simulation, chademo_charging_simulation


class Structure(BaseModel):
    key: str
    value: str | int | float


router = APIRouter(prefix="/charger")

server_logger = ServerLogger.logger_server
ac_logger = ACChargeSessionLogger.ac_charge_flow_logger
chademo_logger = CHADEMOChargeSessionLogger.chademo_charge_flow_logger


@router.get("/all")
async def read_items():
    try:
        server_logger.info("PROPERLY READED SETTINGS")
        return Charger.settings
    except Exception as e:
        server_logger.error(e)
        return {"response": False, "error": e}


@router.get("/outlets")
async def read_outlets():
    return Charger._outlet_in_use_


@router.get("/energy_ongoing_chademo")
async def is_energy_ongoing_chademo():
    if Charger._energy_is_send_loop_chademo_ != 0:
        return True
    else:
        return False


@router.get("/energy_ongoing_ac")
async def is_energy_ongoing_ac():
    if Charger._energy_is_send_loop_ac_ != 0:
        return True
    else:
        return False


@router.get("/get/{item_id}")
async def read_item(item_id: str):
    if item_id not in Charger.settings:
        server_logger.error(f"'{item_id}' CAN'T BE FINDED IN CHARGER!")
        raise HTTPException(status_code=404, detail="REQUEST CAN'T BE FIND!")
    return Charger.settings[item_id]


@router.post("/start_chademo")
async def start_chademo():
    if Vehicle._connected_chademo_:
        try:
            initialize_charge_simulation = chademo_charging_simulation.ChademoVehicle()
            thread = Thread(target=initialize_charge_simulation.prepare_chademo_charging)
            thread.start()
            chademo_logger.info("CHADEMO SESSION INITIALIZE...")
            return {"response": True, "error": None}
        except Exception as e:
            chademo_logger.error(f"UNABLE TO INITIALIZE SESSION! {e}")
            return {"response": False, "error": e}
    chademo_logger.warning("TO START SESSION FIRST CONNECT VEHICLE!")
    raise HTTPException(status_code=404, detail="REQUEST CAN'T BE FIND!")


@router.post("/start_chademo_{percent}")
async def start_chademo_custom(percent: int):
    if Vehicle._connected_chademo_:
        if percent > 100:
            ac_logger.error("PERCENT SHOULD BE 100 OR LOWER!")
            raise HTTPException(status_code=404, detail="UNABLE TO PERFORM CHARGE SESSION")
        else:
            try:
                initialize_charge_simulation = chademo_charging_simulation.ChademoVehicle()
                chademo_logger.info(f"CUSTOM CHARGING LEVEL SET TO: {percent}%")
                thread = Thread(
                    target=initialize_charge_simulation.prepare_chademo_charging,
                    args=[percent],
                )
                chademo_logger.info("SESSION INITIALIZE...")
                thread.start()
                time.sleep(0.2)
                return {"response": True, "error": None}
            except Exception as e:
                chademo_logger.error(f"UNABLE TO INITIALIZE SESSION! {e}")
                return {"response": False, "error": e}
    chademo_logger.warning("TO START SESSION FIRST CONNECT VEHICLE!")
    raise HTTPException(status_code=404, detail="REQUEST CAN'T BE FIND!")


@router.post("/start_ac")
async def start_ac():
    if Vehicle._connected_ac_:
        try:
            initialize_charge_simulation = ac_charge_simulation.AcVehicle()
            thread = Thread(target=initialize_charge_simulation.prepare_ac_charging)
            thread.start()
            ac_logger.info("AC SESSION INITIALIZE...")
            return {"response": True, "error": None}
        except Exception as e:
            ac_logger.error(f"UNABLE TO INITIALIZE SESSION! {e}")
            return {"response": False, "error": e}
    ac_logger.warning("TO START SESSION FIRST CONNECT VEHICLE!")
    raise HTTPException(status_code=404, detail="REQUEST CAN'T BE FIND!")


@router.post("/start_ac_{percent}")
async def start_ac_custom(percent: int):
    if Vehicle._connected_ac_:
        if percent > 100:
            ac_logger.error("PERCENT SHOULD BE 100 OR LOWER!")
            raise HTTPException(status_code=404, detail="UNABLE TO PERFORM CHARGE SESSION")
        else:
            try:
                initialize_charge_simulation = ac_charge_simulation.AcVehicle()
                ac_logger.info(f"CUSTOM CHARGING LEVEL SET TO: {percent}%")
                thread = Thread(
                    target=initialize_charge_simulation.prepare_ac_charging,
                    args=[percent],
                )
                ac_logger.info("SESSION INITIALIZE...")
                thread.start()
                time.sleep(0.2)
                return {"response": True, "error": None}
            except Exception as e:
                ac_logger.error(f"UNABLE TO INITIALIZE SESSION! {e}")
                return {"response": False, "error": e}
    ac_logger.warning("TO START SESSION FIRST CONNECT VEHICLE!")
    raise HTTPException(status_code=404, detail="REQUEST CAN'T BE FIND!")


@router.get("/vehicle_disconnected_{outlet}")
async def vehicle_disconnected(outlet: str):
    print(f"first {outlet}")
    if outlet == "AC":
        print(f"{outlet}")
        Charger._outlet_in_use_[outlet] = "Not used"
        Vehicle._connected_ac_ = False
        Vehicle.settings_ac = None
    if outlet == "CHADEMO":
        Charger._outlet_in_use_[outlet] = "Not used"
        Vehicle._connected_chademo_ = False
        Vehicle.settings_chademo = None


@router.put("/")
async def update_item(struc: Structure):
    if struc.key in Charger.settings:
        try:
            Charger.settings[struc.key] = struc.value
            server_logger.info(f"{struc.key}={struc.value} SETTING PROLERLY CHANGED...")
            return {"response": True, "error": None}
        except Exception as e:
            server_logger.error("UNABE TO CHANGE SETTING!")
            return {"response": False, "error": e}
    server_logger.error(f"'{struc.key}' NOT EXIST IN CHARGER SETTINGS!")
    raise HTTPException(status_code=404, detail="REQUEST CAN'T BE FIND!")
