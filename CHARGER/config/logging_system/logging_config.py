import logging.handlers
import logging
import datetime
import yaml
from pathlib import Path

current_path = Path(__file__).absolute().parents[2]

class CustomFormatter(logging.Formatter):
    LOG_DIR = f"{current_path}/charger_logs/server_logs/"
    LOG_DIR_AC_CHARGING_SESSION = f"{current_path}/charger_logs/charging_logs/"
    LOG_DIR_CHADEMO_CHARGING_SESSION = f"{current_path}/charger_logs/charging_logs/"

    blue = "\x1b[38;5;39m"
    green = "\x1b[1;32m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    data = "%(asctime)s | "
    level_name = "%(levelname)8s "
    file_and_message = "| (%(filename)s:%(lineno)d) | %(message)s"

    FORMATS = {
        logging.DEBUG:  blue + level_name + reset + file_and_message,
        logging.INFO: green + level_name + reset + file_and_message,
        logging.WARNING: yellow + level_name + reset + file_and_message,
        logging.ERROR: red + level_name + reset + file_and_message,
        logging.CRITICAL: bold_red + level_name + reset + file_and_message,
    }

    FORMATS_save_file = {
        logging.DEBUG: data + level_name + file_and_message,
        logging.INFO: data + level_name + file_and_message,
        logging.WARNING: data + level_name + file_and_message,
        logging.ERROR: data + level_name + file_and_message,
        logging.CRITICAL: data + level_name + file_and_message,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class CustomFormatterSaveFile(CustomFormatter):
    def __init__(self) -> None:
        super().__init__()

    def format(self, record):
        log_fmt = self.FORMATS_save_file.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class ServerLogger:
    with open(f"{current_path}/config/config_files/charger_server_config.yaml", "r+") as f:
        server_config = yaml.safe_load(f)
    logger_server = logging.getLogger()
    logger_server.propagate = False
    logger_server.setLevel(server_config["LOG_LEVEL_CONSOLE"])
    logger_server.handlers = []

    # output custom log format in console
    console = logging.StreamHandler()
    console.setLevel(server_config["LOG_LEVEL_CONSOLE"])
    console.setFormatter(CustomFormatter())

    # save custom logs format to file
    today = datetime.date.today()
    save_in_file = logging.handlers.RotatingFileHandler(
        CustomFormatterSaveFile.LOG_DIR + "charger_server__{}.log".format(today.strftime("%Y_%m_%d"))
    )
    save_in_file.setLevel(server_config["LOG_LEVEL"])
    save_in_file.setFormatter(CustomFormatterSaveFile())

    # Add both handlers to the logger
    logger_server.addHandler(console)
    logger_server.addHandler(save_in_file)



class ACChargeSessionLogger:
    with open(f"{current_path}/config/config_files/charger_server_config.yaml", "r+") as f:
        server_config = yaml.safe_load(f)
    ac_charge_flow_logger = logging.getLogger("ac_flow")
    ac_charge_flow_logger.propagate = False
    ac_charge_flow_logger.setLevel(server_config["LOG_LEVEL_CONSOLE"])
    ac_charge_flow_logger.handlers = []
    # charge_flow_logger = logging.getLogger("charge_flow")
    # output custom log format in console
    console = logging.StreamHandler()
    console.setLevel(server_config["LOG_LEVEL_CONSOLE"])
    console.setFormatter(CustomFormatter())

    # save custom logs format to file
    today = datetime.date.today()
    save_in_file = logging.handlers.RotatingFileHandler(
        CustomFormatterSaveFile.LOG_DIR_AC_CHARGING_SESSION + "ac_flow__{}.log".format(today.strftime("%Y_%m_%d"))
    )
    save_in_file.setLevel(server_config["LOG_LEVEL"])
    save_in_file.setFormatter(CustomFormatterSaveFile())

    # Add both handlers to the logger
    ac_charge_flow_logger.addHandler(console)
    ac_charge_flow_logger.addHandler(save_in_file)


class CHADEMOChargeSessionLogger:
    with open(f"{current_path}/config/config_files/charger_server_config.yaml", "r+") as f:
        server_config = yaml.safe_load(f)
    chademo_charge_flow_logger = logging.getLogger("chademo_flow")
    chademo_charge_flow_logger.propagate = False
    chademo_charge_flow_logger.setLevel(server_config["LOG_LEVEL_CONSOLE"])
    chademo_charge_flow_logger.handlers = []
    # charge_flow_logger = logging.getLogger("charge_flow")
    # output custom log format in console
    console = logging.StreamHandler()
    console.setLevel(server_config["LOG_LEVEL_CONSOLE"])
    console.setFormatter(CustomFormatter())

    # save custom logs format to file
    today = datetime.date.today()
    save_in_file = logging.handlers.RotatingFileHandler(
        CustomFormatterSaveFile.LOG_DIR_CHADEMO_CHARGING_SESSION + "chademo_flow__{}.log".format(today.strftime("%Y_%m_%d"))
    )
    save_in_file.setLevel(server_config["LOG_LEVEL"])
    save_in_file.setFormatter(CustomFormatterSaveFile())

    # Add both handlers to the logger
    chademo_charge_flow_logger.addHandler(console)
    chademo_charge_flow_logger.addHandler(save_in_file)
    