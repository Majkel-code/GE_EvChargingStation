*** Variables ***
# JSON Schema files for CHARGER
${GLOBAL_SCHEMA_CHARGER_GET_ALL}                            ${CURDIR}/../schemas/charger/charger_get_all.json 
${GLOBAL_SCHEMA_CHARGER_GET_SPECIFIC}                       ${CURDIR}/../schemas/charger/charger_get_specific.json
${GLOBAL_SCHEMA_CHARGER_GET_SPECIFIC_NEGATIVE}              ${CURDIR}/../schemas/charger/charger_get_specific_negative.json
${GLOBAL_SCHEMA_CHARGER_USED_OUTLETS}                       ${CURDIR}/../schemas/charger/charger_used_outlets.json
${GLOBAL_SCHEMA_CHARGER_UNABLE_AUTHORIZED}                  ${CURDIR}/../schemas/charger/charger_unable_authorization.json
${GLOBAL_SCHEMA_CHARGER_SERVER_ALIVE}                       ${CURDIR}/../schemas/charger/charger_server_alive.json
${GLOBAL_SCHEMA_CHARGER_SESSION_AC_FINISHED}                ${CURDIR}/../schemas/charger/charger_session_ac_finished.json
${GLOBAL_SCHEMA_CHARGER_SESSION_CHADEMO_FINISHED}           ${CURDIR}/../schemas/charger/charger_session_chademo_finished.json
${GLOBAL_SCHEMA_CHARGER_SESSION_ABOVE_LIMIT}                ${CURDIR}/../schemas/charger/charger_session_above_limit.json

# JSON Schema files for CONNECTOR
${GLOBAL_SCHEMA_CHARGER_CONNECT_VEHICLE}                    ${CURDIR}/../schemas/charger/charger_connect_vehicle.json
${GLOBAL_SCHEMA_CHARGER_DISCONNECT_VEHICLE}                 ${CURDIR}/../schemas/charger/charger_disconnect_vehicle.json
${GLOBAL_SCHEMA_CHARGER_ACTUAL_CONNECTED}                   ${CURDIR}/../schemas/charger/charger_actual_connected.json

# JSON Schema files for VEHICLE
${GLOBAL_SCHEMA_VEHICLE_GET_ALL}                            ${CURDIR}/../schemas/vehicle/vehicle_get_all.json 
${GLOBAL_SCHEMA_VEHICLE_GET_SPECIFIC}                       ${CURDIR}/../schemas/vehicle/vehicle_get_specific.json
${GLOBAL_SCHEMA_VEHICLE_GET_SPECIFIC_NEGATIVE}              ${CURDIR}/../schemas/vehicle/vehicle_get_specific_negative.json