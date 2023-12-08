import logging.handlers
import logging
import datetime
import yaml


class CustomFormatter(logging.Formatter):
    LOG_DIR = "server_logs/"

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
        logging.DEBUG: data + blue + level_name + reset + file_and_message,
        logging.INFO: data + green + level_name + reset + file_and_message,
        logging.WARNING: data + yellow + level_name + reset + file_and_message,
        logging.ERROR: data + red + level_name + reset + file_and_message,
        logging.CRITICAL: data + bold_red + level_name + reset + file_and_message,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class Logger:
    with open(f"config/config_files/server_config.yaml", "r+") as f:
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
        CustomFormatter.LOG_DIR + "server_application{}.log".format(today.strftime("%Y_%m_%d"))
    )
    save_in_file.setLevel(server_config["LOG_LEVEL"])
    save_in_file.setFormatter(CustomFormatter())

    # Add both handlers to the logger
    logger.addHandler(console)
    logger.addHandler(save_in_file)


class ServerLogger(Logger):
    pass
