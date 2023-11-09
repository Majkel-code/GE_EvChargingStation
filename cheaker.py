from charger_vehicle_config_bridge import __IsServerAlive__ as server
from logging_config import Logger

logger= Logger.logger

def check_server_is_alive():
    return server._is_alive_



