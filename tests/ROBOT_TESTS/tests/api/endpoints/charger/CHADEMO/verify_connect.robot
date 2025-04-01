*** Settings ***
Resource    ../../../../../testdata/variables/imports.resource
Resource    ../../../../../keywords/imports.resource
Resource    ../charger_keywords/charger_requests.robot

Library    RequestsLibrary

Suite Teardown    SETUP DISCONNECT VEHICLE    ${GLOBAL_ENDPOINT_CHARGER_DISCONNECT_CHADEMO}

*** Test Cases ***
Verify VEHICLE CHADEMO get all
    Log To Console    \nSending Request to ${GLOBAL_ENDPOINT_CHARGER_CONNECT_CHADEMO}\n
    CONNECT VEHICLE    endpoint=${GLOBAL_ENDPOINT_CHARGER_CONNECT_CHADEMO}    schema=${GLOBAL_SCHEMA_CHARGER_CONNECT_VEHICLE}



    