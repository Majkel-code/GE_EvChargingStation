import config.config_reader.read_default_settings as read_default_settings


class ChargerBridge:
	_charging_finished_ = False
	_energy_is_send_loop_ = 0
	settings = read_default_settings.read_charger_settings()


class VehicleBridge:
	_connected_ = False
	settings = read_default_settings.read_vehicle_settings()


class __IsServerAlive__:
	_is_alive_ = False
