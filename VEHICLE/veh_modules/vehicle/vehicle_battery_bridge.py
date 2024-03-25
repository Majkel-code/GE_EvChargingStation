from veh_config.vehicle_config_bridge import VehicleBridge as Vehicle
from veh_modules.battery.AC.ac_battery import AcVehicleSpecification
from veh_modules.battery.CHADEMO.chademo_battery import ChademoVehicleSpecification
import requests

class VehicleBatteryBridge:
    ac_vehicle_spec = AcVehicleSpecification()
    chademo_vehicle_spec = ChademoVehicleSpecification()

    def send_kw_to_battery(outlet, kw_min):
        if outlet == "AC":
            VehicleBatteryBridge.ac_vehicle_spec.actual_kw_per_min = kw_min
            VehicleBatteryBridge.ac_vehicle_spec.calculate_battery_increase()
        elif outlet == "CHADEMO":
            VehicleBatteryBridge.chademo_vehicle_spec.actual_kw_per_min = kw_min
            VehicleBatteryBridge.chademo_vehicle_spec.calculate_battery_increase()
    
    def save_after_server_shutdown():
        if Vehicle.settings_ac["SESSION_ID"] is not None:
            VehicleBatteryBridge.perform_charge_saver("AC")
            url = "http://127.0.0.1:5000/charger/vehicle_disconnected_AC"
            headers = {"Content-Type": "application/json"}
            response = requests.get(url, headers=headers)
        if Vehicle.settings_chademo["SESSION_ID"] is not None:
            VehicleBatteryBridge.perform_charge_saver("CHADEMO")

    def perform_charge_saver(outlet):
        if outlet == "AC":
            print("IN AC SAVER")
            VehicleBatteryBridge.ac_vehicle_spec.perform_charge_saver()
            Vehicle.ac_load_configuration()
            VehicleBatteryBridge.ac_vehicle_spec = AcVehicleSpecification()
        elif outlet == "CHADEMO":
            VehicleBatteryBridge.chademo_vehicle_spec.perform_charge_saver()
            Vehicle.chademo_load_configuration()
            VehicleBatteryBridge.chademo_vehicle_spec = ChademoVehicleSpecification()

    def reload_vehicle_specification(outlet):
        if outlet == "AC":
            VehicleBatteryBridge.ac_vehicle_spec = AcVehicleSpecification()
        elif outlet == "CHADEMO":
            VehicleBatteryBridge.chademo_vehicle_spec = ChademoVehicleSpecification()

    def read_charge_history(outlet):
        return AcVehicleSpecification.open_session_history(outlet=outlet)
