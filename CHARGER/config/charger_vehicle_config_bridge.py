import json
import secrets

import config.config_reader.read_default_settings as read_default_settings
import requests


class ChargerBridge:

    _charging_finished_chademo_ = False
    _charging_finished_ac_ = False
    _energy_is_send_loop_chademo_ = 0
    _energy_is_send_loop_ac_ = 0
    settings = read_default_settings.read_charger_settings()
    _outlet_in_use_ = {}
    for outlet in settings["CHARGING_OUTLETS"]:
        _outlet_in_use_[outlet] = "Not used"

    def energy_ongoing(outlet):
        if outlet == "AC":
            return ChargerBridge._energy_is_send_loop_ac_
        if outlet == "CHADEMO":
            return ChargerBridge._energy_is_send_loop_chademo_

    def session_finished(outlet):
        if outlet == "AC":
            return ChargerBridge._charging_finished_ac_
        if outlet == "CHADEMO":
            return ChargerBridge._charging_finished_chademo_


class VehicleBridge:
    _connected_chademo_ = False
    _connected_ac_ = False
    settings_chademo = None
    settings_ac = None

    _charged_ac_kw = 0
    _charged_chademo_kw = 0

    def check_connection(outlet):
        if outlet == "AC":
            return VehicleBridge._connected_ac_
        if outlet == "CHADEMO":
            return VehicleBridge._connected_chademo_

    def connect_vehicle(outlet_used):
        try:
            if outlet_used == "CHADEMO":
                try:
                    url = "http://127.0.0.1:5001/handshake_chademo/connect"
                    key = take_vehicle_key()
                    payload = json.dumps({"id": key})
                    headers = {"Content-Type": "application/json"}
                    response = requests.put(url, headers=headers, data=payload)
                    if response.ok:
                        VehicleBridge._connected_chademo_ = True
                        ChargerBridge._outlet_in_use_[outlet_used] = key
                        return {"handshake_chademo": True}
                except Exception:
                    return {"handshake_chademo": False}

            elif outlet_used == "AC":
                try:
                    url = "http://127.0.0.1:5001/handshake_ac/connect"
                    key = take_vehicle_key()
                    payload = json.dumps({"id": key})
                    headers = {"Content-Type": "application/json"}
                    response = requests.put(url, headers=headers, data=payload)
                    if response.ok:
                        VehicleBridge._connected_ac_ = True
                        ChargerBridge._outlet_in_use_[outlet_used] = key
                        return {"handshake_ac": True}
                except Exception:
                    return {"handshake_ac": False}

        except Exception as e:
            return e

    def disconnect_vehicle(outlet_used):
        if outlet_used == "CHADEMO":
            try:
                url = "http://127.0.0.1:5001/handshake_chademo/disconnect"
                payload = json.dumps(
                    {
                        "id": ChargerBridge._outlet_in_use_[outlet_used],
                        "end_connection": True,
                    }
                )
                headers = {"Content-Type": "application/json"}
                response = requests.put(url, headers=headers, data=payload)
                if response.ok:
                    ChargerBridge._outlet_in_use_[outlet_used] = "Not used"
                    VehicleBridge._connected_chademo_ = False
                    VehicleBridge.settings_chademo = None
                    VehicleBridge._charged_chademo_kw = 0
                    return {"disconnect_chademo": True}
            except Exception:
                return {"disconnect_chademo": False}

        elif outlet_used == "AC":
            try:
                url = "http://127.0.0.1:5001/handshake_ac/disconnect"
                payload = json.dumps(
                    {
                        "id": ChargerBridge._outlet_in_use_[outlet_used],
                        "end_connection": True,
                    }
                )
                headers = {"Content-Type": "application/json"}
                response = requests.put(url, headers=headers, data=payload)
                if response.ok:
                    ChargerBridge._outlet_in_use_[outlet_used] = "Not used"
                    VehicleBridge._connected_ac_ = False
                    VehicleBridge.settings_ac = None
                    VehicleBridge._charged_ac_kw = 0
                    return {"disconnect_ac": True}
            except Exception:
                return {"disconnect_ac": False}

    def take_ac_vehicle_specification():
        url = "http://127.0.0.1:5001/vehicle_ac/all"
        headers = {"Content-Type": "application/json"}
        response = requests.get(url, headers=headers)
        veh_data = response.json()
        if veh_data["response"] == "OK":
            VehicleBridge.settings_ac = veh_data["data"]["parameters"]
        return response

    def take_chademo_vehicle_specification():
        url = "http://127.0.0.1:5001/vehicle_chademo/all"
        headers = {"Content-Type": "application/json"}
        response = requests.get(url, headers=headers)
        veh_data = response.json()
        if veh_data["response"] == "OK":
            VehicleBridge.settings_chademo = veh_data["data"]["parameters"]
        return response

    def session_complete_chademo():
        url = "http://127.0.0.1:5001/vehicle_chademo/chademo_complete"
        payload = {"complete": ChargerBridge._charging_finished_chademo_}
        headers = {"Content-Type": "application/json"}
        requests.patch(url, headers=headers, data=json.dumps(payload))

    def session_complete_ac():
        url = "http://127.0.0.1:5001/vehicle_ac/ac_complete"
        payload = {"complete": ChargerBridge._charging_finished_ac_}
        headers = {"Content-Type": "application/json"}
        requests.patch(url, headers=headers, data=json.dumps(payload))


class IsServerAlive:
    _is_alive_ = False

    def check_server_is_alive():
        return IsServerAlive._is_alive_


def take_vehicle_key():
    key = secrets.token_hex(32)
    return key
