*** Settings ***
Resource    ../../../../../testdata/variables/imports.resource
Resource    ../../../../../keywords/imports.resource
Resource    ../vehicle_keywords/vehicle_requests.robot

Library    RequestsLibrary

Test Template    Custom Test Template

*** Test Cases ***                                    OPTION
Verify VEHICLE CHADEMO SESSION_ID                          SESSION_ID
Verify VEHICLE CHADEMO BATTERY_LEVEL                       BATTERY_LEVEL
Verify VEHICLE CHADEMO CHARGING_PORT                       CHARGING_PORT
Verify VEHICLE CHADEMO MAX_BATTERY_CAPACITY_IN_KWH         MAX_BATTERY_CAPACITY_IN_KWH
Verify VEHICLE CHADEMO ACTUAL_BATTERY_STATUS_IN_KWH        ACTUAL_BATTERY_STATUS_IN_KWH
Verify VEHICLE CHADEMO BATTERY_VOLTAGE                     BATTERY_VOLTAGE
Verify VEHICLE CHADEMO COOLING_SYSTEM                      COOLING_SYSTEM
Verify VEHICLE CHADEMO EFFECTIVE_CHARGING_CAP              EFFECTIVE_CHARGING_CAP

*** Keywords ***
Custom Test Template
    [Arguments]    ${option}
    Log To Console    \nSending Request to ${GLOBAL_ENDPOINT_VEHICLE_CHADEMO_GET_SPECIFIC}/${option}\n
    VEHICLE get specific    endpoint=${GLOBAL_ENDPOINT_VEHICLE_CHADEMO_GET_SPECIFIC}    schema=${GLOBAL_SCHEMA_VEHICLE_GET_SPECIFIC}    option=${option}
