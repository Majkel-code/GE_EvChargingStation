import config.config_reader.read_default_settings as read_default_settings
import secrets
import requests
import json

class ChargerBridge:
    _charging_finished_chademo_ = False
    _charging_finished_ac_ = False
    _energy_is_send_loop_chademo_ = 0
    _energy_is_send_loop_ac_ = 0
    settings = read_default_settings.read_charger_settings()
    _outlet_in_use_ = {}
    for outlet in settings["CHARGING_OUTLETS"]:
        _outlet_in_use_[outlet] = "Not used"




class VehicleBridge:
    _connected_chademo_ = False
    _connected_ac_ = False
    settings_chademo = None
    settings_ac = None

    def connect_vehicle(outlet_used):
        try:
            if outlet_used == "CHADEMO":
                url = "http://127.0.0.1:5001/handshake_chademo/connect"
                key = take_vehicle_key()
                payload = json.dumps({
                "id": key
                })
                headers = {
                'Content-Type': 'application/json'
                }
                response = requests.put(url, headers=headers, data=payload)

                print(response)
                if response.ok:
                    VehicleBridge._connected_chademo_ = True
                    ChargerBridge._outlet_in_use_[outlet_used] = key
                return response
                
            elif outlet_used == "AC":
                url = "http://127.0.0.1:5001/handshake_ac/connect"
                key = take_vehicle_key()
                payload = json.dumps({
                "id": key
                })
                headers = {
                'Content-Type': 'application/json'
                }
                response = requests.put(url, headers=headers, data=payload)

                print(response)
                if response.ok:
                    VehicleBridge._connected_ac_ = True
                    ChargerBridge._outlet_in_use_[outlet_used] = key
                return response
                

        except Exception as e:
            return e

    def disconnect_vehicle(outlet_used):
        if outlet_used == "CHADEMO":
            url = "http://127.0.0.1:5001/handshake_chademo/disconnect"
            payload = json.dumps({
            "id":  ChargerBridge._outlet_in_use_[outlet_used],
            "end_connection": True
            })
            headers = {
            'Content-Type': 'application/json'
            }
            response = requests.put(url, headers=headers, data=payload)
            if response.ok:
                ChargerBridge._outlet_in_use_[outlet_used] = "Not used"
                VehicleBridge._connected_chademo_ = False
                VehicleBridge.settings_chademo = None
            return response

        elif outlet_used == "AC":
            url = "http://127.0.0.1:5001/handshake_ac/disconnect"
            payload = json.dumps({
            "id":  ChargerBridge._outlet_in_use_[outlet_used],
            "end_connection": True
            })
            headers = {
            'Content-Type': 'application/json'
            }
            response = requests.put(url, headers=headers, data=payload)
            if response.ok:
                ChargerBridge._outlet_in_use_[outlet_used] = "Not used"
                VehicleBridge._connected_ac_ = False
                VehicleBridge.settings_ac = None
            return response
        

    def take_ac_vehicle_specification():
        url = "http://127.0.0.1:5001/vehicle_ac/all"
        # payload = json.dumps({
        # "id":  ChargerBridge._outlet_in_use_[outlet_used],
        # "end_connection": True
        # })
        headers = {
        'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        if response.ok:
            VehicleBridge.settings_ac = response.json()
        return response
    
    def take_chademo_vehicle_specification():
        url = "http://127.0.0.1:5001/vehicle_chademo/all"
        # payload = json.dumps({
        # "id":  ChargerBridge._outlet_in_use_[outlet_used],
        # "end_connection": True
        # })
        headers = {
        'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        if response.ok:
            VehicleBridge.settings_chademo = response.json()
        return response


class IsServerAlive:
    _is_alive_ = False

    def check_server_is_alive():
        return IsServerAlive._is_alive_


def take_vehicle_key():
    key = secrets.token_hex(32)
    return key
