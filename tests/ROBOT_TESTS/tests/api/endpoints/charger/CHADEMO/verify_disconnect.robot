*** Settings ***
Resource    ../../../../../testdata/variables/imports.resource
Resource    ../../../../../keywords/imports.resource
Resource    ../charger_keywords/charger_requests.robot

Library    RequestsLibrary

Suite Setup    SETUP CONNECT VEHICLE    ${GLOBAL_ENDPOINT_CHARGER_CONNECT_CHADEMO}

*** Test Cases ***
Verify VEHICLE CHADEMO get all
    Log To Console    \nSending Request to ${GLOBAL_ENDPOINT_CHARGER_DISCONNECT_CHADEMO}\n
    DISCONNECT VEHICLE    endpoint=${GLOBAL_ENDPOINT_CHARGER_DISCONNECT_CHADEMO}    schema=${GLOBAL_SCHEMA_CHARGER_DISCONNECT_VEHICLE}



    