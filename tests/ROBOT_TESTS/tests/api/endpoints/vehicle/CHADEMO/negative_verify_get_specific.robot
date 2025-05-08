*** Settings ***
Resource    ../../../../../testdata/variables/imports.resource
Resource    ../../../../../keywords/imports.resource
Resource    ../vehicle_keywords/vehicle_requests.robot

Library    RequestsLibrary

*** Test Cases ***
Verify negative get specific key
    Log To Console    \nSending Request to ${GLOBAL_ENDPOINT_VEHICLE_CHADEMO_GET_SPECIFIC_NEGATIVE}\n
    VEHICLE get specific negative    endpoint=${GLOBAL_ENDPOINT_VEHICLE_CHADEMO_GET_SPECIFIC_NEGATIVE}    schema=${GLOBAL_SCHEMA_VEHICLE_GET_SPECIFIC_NEGATIVE}
