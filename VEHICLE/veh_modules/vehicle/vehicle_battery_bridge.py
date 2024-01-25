from veh_config.vehicle_config_bridge import VehicleBridge as Vehicle
from veh_modules.battery.AC.ac_battery import AcVehicleSpecification
from veh_modules.battery.CHADEMO.chademo_battery import ChademoVehicleSpecification


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

    def perform_charge_saver(outlet):
        if outlet == "AC":
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
