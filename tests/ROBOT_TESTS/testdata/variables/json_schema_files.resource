*** Variables ***
# JSON Schema files for CHARGER
${GLOBAL_SCHEMA_CHARGER_GET_ALL}                ${CURDIR}/../schemas/charger/charger_get_all.json 
${GLOBAL_SCHEMA_CHARGER_GET_SPECIFIC}           ${CURDIR}/../schemas/charger/charger_get_specific.json
${GLOBAL_SCHEMA_CHARGER_GET_SPECIFIC_NEGATIVE}  ${CURDIR}/../schemas/charger/charger_get_specific_negative.json
${GLOBAL_SCHEMA_CHARGER_USED_OUTLETS}           ${CURDIR}/../schemas/charger/charger_used_outlets.json
${GLOBAL_SCHEMA_CHARGER_UNABLE_AUTHORIZED}      ${CURDIR}/../schemas/charger/charger_unable_authorization.json
${GLOBAL_SCHEMA_CHARGER_SERVER_ALIVE}           ${CURDIR}/../schemas/charger/charger_server_alive.json

# JSON Schema files for VEHICLE
${GLOBAL_SCHEMA_VEHICLE_AC_GET_ALL}                ${CURDIR}/../schemas/vehicle/vehicle_get_all.json 
${GLOBAL_SCHEMA_VEHICLE_AC_GET_SPECIFIC}           ${CURDIR}/../schemas/vehicle/vehicle_get_specific.json
${GLOBAL_SCHEMA_VEHICLE_AC_GET_SPECIFIC_NEGATIVE}  ${CURDIR}/../schemas/vehicle/vehicle_get_specific_negative.json