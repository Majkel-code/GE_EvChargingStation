from pathlib import Path
import asyncio
import sys
import multiprocessing
from multiprocessing import Process, Queue
import time
import os
import signal

import config.charger_vehicle_config_bridge as charger_vehicle_config_bridge
import modules.charger.charger as charger
import modules.vehicle.vehicle_ac_connect as vehicle_ac_connect
import modules.vehicle.vehicle_chademo_connect as vehicle_chademo_connect
import uvicorn
import yaml
from config.charger_vehicle_config_bridge import IsServerAlive as _main_server
from config.config_reader.generate_auth_key import AuthorizationSystem
from config.logging_system.logging_config import ServerLogger
from fastapi import FastAPI, Request
from modules.display import display_ac, display_chademo

server_logger = ServerLogger.logger_server

class InitialiseServer:
    def __init__(self, q,) -> None:
        try:
            self._status = {
                "is_alive": False,
                "restart": False,
                "shutdown": False,
                "shutdown_complete": False,
            }
            self.app = FastAPI()
            self.app.include_router(charger.router)
            self.app.include_router(vehicle_ac_connect.router)
            self.app.include_router(vehicle_chademo_connect.router)
            self.app.include_router(display_ac.router)
            self.app.include_router(display_chademo.router)
            self.server = uvicorn.Server
            charger_vehicle_config_bridge.ChargerBridge()
            current_path = Path(__file__).absolute().parent
            config_path = f"{current_path}/config/config_files"
            with open(
                f"{config_path}/charger_server_config.yaml",
                "r+",
            ) as f:
                server_config = yaml.safe_load(f)
            # if server_config_addons is not None:
            #     server_config["LOG_LEVEL_SERVER"] = server_config_addons["LOG_LEVEL_SERVER"]
            #     server_config["LOG_LEVEL_CONSOLE"] = server_config_addons["LOG_LEVEL_CONSOLE"]
            #     server_config["LOG_LEVEL"] = server_config_addons["LOG_LEVEL"]
            self.auth = AuthorizationSystem(os.getcwd())
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
                    await asyncio.sleep(1)

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
                    server_logger.warning("RESTART")
                else:
                    server_logger.warning("SHUTDOWN")
                for i in range(5):
                    server_logger.warning("SHUTTING DOWN IN {} SECONDS".format(5 - i))
                    await asyncio.sleep(1)
                self._status["shutdown_complete"] = True
                os.kill(os.getpid(), signal.SIGINT)


            @self.app.on_event("startup")
            async def startup_event():
                loop = asyncio.get_running_loop()
                loop.create_task(mainloop())


            @self.app.on_event("shutdown")
            async def shutdown_event():
                # hook shutdown event
                self._status["shutdown"] = True
                while self._status["shutdown_complete"] is False:
                    await asyncio.sleep(1)


            @self.app.get("/{name}")
            async def check(name: str, request: Request):
                data_to_return = None
                key = request.headers.get("authorization")
                if self.auth.read_local_key() == key:

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

                    elif name == "ac_connect":
                        data_to_return = (
                            charger_vehicle_config_bridge.VehicleBridge.check_connection("AC")
                        )

                    elif name == "chademo_connect":
                        data_to_return = (
                            charger_vehicle_config_bridge.VehicleBridge.check_connection("CHADEMO")
                        )

                    elif name == "ac_charging_ongoing":
                        data_to_return = charger_vehicle_config_bridge.ChargerBridge.energy_ongoing(
                            "AC"
                        )

                    elif name == "chademo_charging_ongoing":
                        data_to_return = charger_vehicle_config_bridge.ChargerBridge.energy_ongoing(
                            "CHADEMO"
                        )

                    elif name == "ac_finished":
                        data_to_return = (
                            charger_vehicle_config_bridge.ChargerBridge.session_finished("AC")
                        )

                    elif name == "chademo_finished":
                        data_to_return = (
                            charger_vehicle_config_bridge.ChargerBridge.session_finished("CHADEMO")
                        )

                    elif name == "reload_settings_ac":
                        data_to_return = (
                            charger_vehicle_config_bridge.VehicleBridge.take_ac_vehicle_specification().ok
                        )

                    elif name == "reload_settings_chademo":
                        data_to_return = (
                            charger_vehicle_config_bridge.VehicleBridge.take_chademo_vehicle_specification().ok
                        )
                else:
                    server_logger.error("UNABLE TO AUTHORIZE REQUEST!")
                    return {
                        "response": "NOK",
                        "error": "UNABLE TO AUTHORIZE REQUEST!",
                        "data": None,
                    }
                return {
                        "response": "OK",
                        "error": None,
                        "data": {f"{name}": data_to_return},
                    }

        except Exception as e:
            server_logger.error(e)


class Server(InitialiseServer):
    def __init__(self, q):
        super().__init__(q)

        if not _main_server._is_alive_:
            try:
                _main_server._is_alive_ = True
                self.server = self.server(self.config)
                self.server.run()
                server_logger.info("SERVER CLOSED SUCCESSFUL!")
                _main_server._is_alive_ = False
            except Exception as e:
                server_logger.critical(f"UNABLE TO ESTABLISH SERVER! {e}")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    start = Server
    q = Queue()
    child = Process(target=start, args=(q,))
    # start the child process
    child.start()

    while True:
        time.sleep(1)
        child.join()
        server_status = q.get()
        if server_status["restart"] == True:
            for i in range(5):
                server_logger.info("RESTARTING APPLICATION IN {} SECONDS".format(5 - i))
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

