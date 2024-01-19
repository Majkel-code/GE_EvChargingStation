import config.config_reader.read_default_settings as read_default_settings


class VehicleBridge:
    settings_chademo = None
    settings_ac = None
    settings_chademo = read_default_settings.read_vehicle_chademo_settings()
    settings_ac = read_default_settings.read_vehicle_ac_settings()


class IsServerAlive:
    _is_alive_ = False

    def check_server_is_alive():
        return IsServerAlive._is_alive_
