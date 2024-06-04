import veh_config.config_reader.read_default_settings as read_default_settings


class VehicleBridge:
    settings_chademo = read_default_settings.read_vehicle_chademo_settings()
    settings_ac = read_default_settings.read_vehicle_ac_settings()

    def ac_load_configuration():
        VehicleBridge.settings_ac = read_default_settings.read_vehicle_ac_settings()

    def chademo_load_configuration():
        VehicleBridge.settings_chademo = read_default_settings.read_vehicle_chademo_settings()

    def perform_session_saver():
        VehicleBridge.ac_veh.perform_charge_saver()


class IsServerAlive:
    _is_alive_ = False

    def check_server_is_alive():
        return IsServerAlive._is_alive_
