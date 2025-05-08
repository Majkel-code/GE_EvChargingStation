from pathlib import Path
import asyncio
import sys
import multiprocessing
from multiprocessing import Process, Queue
import time
import os
import signal
import uvicorn
import veh_modules.vehicle.handshakes.ac_handshake as ac_handshake
import veh_modules.vehicle.handshakes.chademo_handshake as chademo_handshake
import veh_modules.vehicle.vehicle_ac_simulator as vehicle_ac_simulator
import veh_modules.vehicle.vehicle_chademo_simulator as vehicle_chademo_simulator
import yaml
from fastapi import FastAPI
from veh_config.logging_system.logging_config import Logger
from veh_config.vehicle_config_bridge import IsServerAlive as _main_server
from veh_config.vehicle_config_bridge import VehicleBridge
from veh_modules.battery.AC.ac_battery import AcVehicleSpecification
from veh_modules.battery.CHADEMO.chademo_battery import ChademoVehicleSpecification
from veh_modules.vehicle.vehicle_battery_bridge import VehicleBatteryBridge

logger = Logger.logger


class InitialiseServer:
    def __init__(self,q,) -> None:
        try:
            self._status = {
                "is_alive": False,
                "restart": False,
                "shutdown": False,
                "shutdown_complete": False,
            }
            self.app = FastAPI()
            VehicleBridge.ac_load_configuration()
            VehicleBridge.chademo_load_configuration()
            self.app.include_router(vehicle_ac_simulator.router)
            self.app.include_router(vehicle_chademo_simulator.router)
            self.app.include_router(ac_handshake.router)
            self.app.include_router(chademo_handshake.router)
            VehicleBatteryBridge.ac_vehicle_spec = AcVehicleSpecification()
            VehicleBatteryBridge.chademo_vehicle_spec = ChademoVehicleSpecification()
            self.server = uvicorn.Server
            current_path = Path(__file__).absolute().parent
            with open(
                f"{current_path}/veh_config/config_files/vehicle_server_config.yaml",
                "r+",
            ) as f:
                server_config = yaml.safe_load(f)
            self.config = uvicorn.Config(
                app=self.app,
                port=server_config["PORT"],
                log_config=None,
                log_level=server_config["LOG_LEVEL_SERVER"],
                host=server_config["HOST_IP"],
                reload=server_config["RELOAD"],
            )

            async def worker(n):
                while not self._status["shutdown"]:
                    await asyncio.sleep(0.1)


            async def mainloop():
                loop = asyncio.get_running_loop()
                done = []
                pending = [loop.create_task(worker(1)), loop.create_task(worker(2))]

                # Handle results in the order the task are completed
                # if exeption you can handle that as well.
                while len(pending) > 0:
                    done, pending = await asyncio.wait(pending)
                    for task in done:
                        sys.tracebacklimit=0
                        e = task.exception()
                        if e is not None:
                            print(f"{e.__class__.__name__}")
                            if e.__class__.__name__ == "RuntimeError":
                                break
                            if e.__class__.__name__ == "KeyboardInterrupt":
                                break

                            # This will print the exception as stack trace
                            task.print_stack()
                        else:
                            result = task.result()
                # This is needed to kill the Uvicorn server and communicate the
                # exit code
                if self._status["restart"]:
                    logger.warning("RESTART")
                else:
                    logger.warning("SHUTDOWN")
                VehicleBatteryBridge.save_after_server_shutdown()
                for i in range(5):
                    logger.warning("SHUTTING DOWN IN {} SECONDS".format(5 - i))
                    await asyncio.sleep(1)
                self._status["shutdown_complete"] = True
                os.kill(os.getpid(), signal.SIGINT)

            @self.app.on_event("startup")
            async def startup_event():
                loop = asyncio.get_running_loop()
                loop.create_task(mainloop())


            @self.app.on_event("shutdown")
            async def shutdown_event():
                # This is a hook point where the event
                # loop has completely shut down
                self._status["shutdown"] = True
                while self._status["shutdown_complete"] is False:
                    await asyncio.sleep(1)


            @self.app.get("/{name}")
            async def veh_check(name: str):
                data_to_return = None

                if name == "shutdown":
                    self._status["shutdown"] = True
                    data_to_return = True
                    q.put(self._status)

                if name == "restart":
                    self._status["restart"] = True
                    self._status["shutdown"] = True
                    data_to_return = True
                    q.put(self._status)

                if name == "is_alive":
                    data_to_return = _main_server.check_server_is_alive()

                if name == "reload_ac":
                    VehicleBridge.ac_load_configuration()
                    AcVehicleSpecification()
                    data_to_return = True

                if name == "reload_chademo":
                    VehicleBridge.chademo_load_configuration()
                    ChademoVehicleSpecification()
                    data_to_return = True

                if name == "ac_history":
                    return AcVehicleSpecification.read_charge_history(
                        AcVehicleSpecification, outlet="AC"
                    )
                if name == "chademo_history":
                    return ChademoVehicleSpecification.read_charge_history(
                        ChademoVehicleSpecification, outlet="CHADEMO"
                    )

                return {f"{name}": data_to_return}

        except Exception as e:
            logger.error(e)


class Server(InitialiseServer):
    def __init__(self, q):
        super().__init__(q)

        if not _main_server._is_alive_:
            try:
                _main_server._is_alive_ = True
                self.server = self.server(self.config)
                self.server.run()
                VehicleBatteryBridge.save_after_server_shutdown()
                logger.info("SERVER CLOSED SUCCESSFUL!")
                _main_server._is_alive_ = False
            except Exception as e:
                _main_server._is_alive_ = False
                logger.critical(f"UNABLE TO ESTABLISH SERVER! {e}")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    start = Server
    q = Queue()
    # create a child process
    child = Process(target=start, args=(q,))
    # start the child process
    child.start()
    while True:
        time.sleep(1)
        child.join()
        server_status = q.get()
        if server_status["restart"] == True:
            for i in range(5):
                logger.info("RESTARTING APPLICATION IN {} SECONDS".format(5 - i))
                time.sleep(1)
            start = Server
            child = Process(target=start, args=(q,))
            child.start()
        elif server_status["shutdown"] == True:
            sys.exit(0)
        elif server_status["is_alive"] == False and server_status["shutdown"] == False and server_status["restart"] == False:
            for i in range(5):
                print("SERVER IS NOT ALIVE! RESTARTING IN {} SECONDS".format(5 - i))
                time.sleep(1)
            start = Server
            child = Process(target=start, args=(q,))
            child.start()
