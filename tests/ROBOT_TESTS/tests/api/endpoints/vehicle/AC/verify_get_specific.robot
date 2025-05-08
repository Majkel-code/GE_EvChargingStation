*** Settings ***
Resource    ../../../../../testdata/variables/imports.resource
Resource    ../../../../../keywords/imports.resource
Resource    ../vehicle_keywords/vehicle_requests.robot

Library    RequestsLibrary

Test Template    Custom Test Template

*** Test Cases ***                                    OPTION
Verify VEHICLE AC SESSION_ID                          SESSION_ID
Verify VEHICLE AC BATTERY_LEVEL                       BATTERY_LEVEL
Verify VEHICLE AC CHARGING_PORT                       CHARGING_PORT
Verify VEHICLE AC MAX_BATTERY_CAPACITY_IN_KWH         MAX_BATTERY_CAPACITY_IN_KWH
Verify VEHICLE AC ACTUAL_BATTERY_STATUS_IN_KWH        ACTUAL_BATTERY_STATUS_IN_KWH
Verify VEHICLE AC BATTERY_VOLTAGE                     BATTERY_VOLTAGE
Verify VEHICLE AC COOLING_SYSTEM                      COOLING_SYSTEM
Verify VEHICLE AC EFFECTIVE_CHARGING_CAP              EFFECTIVE_CHARGING_CAP

*** Keywords ***
Custom Test Template
    [Arguments]    ${option}
    Log To Console    \nSending Request to ${GLOBAL_ENDPOINT_VEHICLE_AC_GET_SPECIFIC}/${option}\n
    VEHICLE get specific    endpoint=${GLOBAL_ENDPOINT_VEHICLE_AC_GET_SPECIFIC}    schema=${GLOBAL_SCHEMA_VEHICLE_GET_SPECIFIC}    option=${option}
    # ${response}    GET    url=${GLOBAL_ENDPOINT_VEHICLE_AC_GET_SPECIFIC}/${option}    expected_status=200
    # Validate Schema    inputJson=${response.json()}    referenceSchemaPath=${GLOBAL_SCHEMA_VEHICLE_AC_GET_SPECIFIC}
