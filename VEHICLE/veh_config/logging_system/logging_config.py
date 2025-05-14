import datetime
import os
import logging
import logging.handlers
from pathlib import Path
from os.path import abspath, normpath
import sys
import yaml

current_path = Path(__file__).absolute().parents[2]

def check_logs_paths(LOG_DIR):
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR, exist_ok=True)
    else:
        pass

class CustomFormatter(logging.Formatter):
    path = normpath(abspath(sys.executable if getattr(sys, 'frozen', False) else os.getcwd()))
    if getattr(sys, 'frozen', False):
        directory_path = os.path.dirname(path)
    else:
        directory_path = path
    LOG_DIR = f"{directory_path}/logs/vehicle/"
    check_logs_paths(LOG_DIR)
    
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
        logging.DEBUG: blue + level_name + reset + file_and_message,
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


class Logger:
    with open(f"{current_path}/veh_config/config_files/vehicle_server_config.yaml", "r+") as f:
        server_config = yaml.safe_load(f)
    logger = logging.getLogger()
    logger.setLevel(server_config["LOG_LEVEL_CONSOLE"])
    logger.handlers = []

    # output custom log format in console
    console = logging.StreamHandler()
    console.setLevel(server_config["LOG_LEVEL_CONSOLE"])
    console.setFormatter(CustomFormatter())

    # save custom logs format to file
    today = datetime.date.today()
    save_in_file = logging.handlers.RotatingFileHandler(
        CustomFormatterSaveFile.LOG_DIR
        + "vehicle_server__{}.log".format(today.strftime("%Y_%m_%d"))
    )
    save_in_file.setLevel(server_config["LOG_LEVEL"])
    save_in_file.setFormatter(CustomFormatterSaveFile())

    # Add both handlers to the logger
    logger.addHandler(console)
    logger.addHandler(save_in_file)
