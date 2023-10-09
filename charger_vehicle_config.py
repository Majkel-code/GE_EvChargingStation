import read_default_settings


class ChargerBridge:
	charging = {"is_finished": False}
	settings = read_default_settings.read_charger_settings()


class VehicleBridge:
	connect = {"is_connected": False}
	settings = read_default_settings.read_vehicle_settings()
