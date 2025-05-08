*** Settings ***
Resource    ../../../../../testdata/variables/imports.resource
Resource    ../../../../../keywords/imports.resource
Resource    ../vehicle_keywords/vehicle_requests.robot

Library    RequestsLibrary

*** Test Cases ***
Verify VEHICLE AC get all
    Log To Console    \nSending Request to ${GLOBAL_ENDPOINT_VEHICLE_CHADEMO_GET_ALL}\n
    VEHICLE get all    endpoint=${GLOBAL_ENDPOINT_VEHICLE_CHADEMO_GET_ALL}    schema=${GLOBAL_SCHEMA_VEHICLE_GET_ALL}



    