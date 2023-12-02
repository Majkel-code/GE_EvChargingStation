import config.config_reader.read_default_settings as read_default_settings
import secrets

class ChargerBridge:
	_charging_finished_chademo_ = False
	_charging_finished_ac_ = False
	_energy_is_send_loop_chademo_ = 0
	_energy_is_send_loop_ac_ = 0
	settings = read_default_settings.read_charger_settings()
	_outlet_in_use_ = {}
	for outlet in settings['CHARGING_OUTLETS']:
		_outlet_in_use_[outlet] = "Not used"


class VehicleBridge:
	_connected_chademo_ = False
	_connected_ac_ = False
	settings_chademo = None
	settings_ac = None


class __IsServerAlive__:
	_is_alive_ = False



def take_vehicle_key():
	key = secrets.token_hex(32)
	return key

def connect_vehicle(outlet_used):
	try:
		if outlet_used == "CHADEMO":
			VehicleBridge._connected_chademo_ = True
			VehicleBridge.settings_chademo = read_default_settings.read_vehicle_chademo_settings()
			key = take_vehicle_key()
			VehicleBridge.settings_chademo["VEHICLE_ID"] = key
			ChargerBridge._outlet_in_use_[outlet_used] = VehicleBridge.settings_chademo["VEHICLE_ID"]
		elif outlet_used == "AC":
			VehicleBridge._connected_ac_ = True
			VehicleBridge.settings_ac = read_default_settings.read_vehicle_ac_settings()
			key = take_vehicle_key()
			VehicleBridge.settings_ac["VEHICLE_ID"] = key
			ChargerBridge._outlet_in_use_[outlet_used] = VehicleBridge.settings_ac["VEHICLE_ID"]
	except Exception as e:
		return e
	
def disconnect_vehicle(outlet_used):
	if outlet_used == "CHADEMO":
		VehicleBridge.settings_chademo = None
		ChargerBridge._outlet_in_use_[outlet_used] = "Not used"
		VehicleBridge._connected_chademo_ = False
	elif outlet_used == "AC":
		VehicleBridge.settings_ac = None
		ChargerBridge._outlet_in_use_[outlet_used] = "Not used"
		VehicleBridge._connected_ac_ = False
