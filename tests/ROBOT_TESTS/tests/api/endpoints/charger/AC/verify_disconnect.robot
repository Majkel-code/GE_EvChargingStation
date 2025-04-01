*** Settings ***
Resource    ../../../../../testdata/variables/imports.resource
Resource    ../../../../../keywords/imports.resource
Resource    ../charger_keywords/charger_requests.robot

Library    RequestsLibrary

Suite Setup    SETUP CONNECT VEHICLE    ${GLOBAL_ENDPOINT_CHARGER_CONNECT_AC}

*** Test Cases ***
Verify VEHICLE AC get all
    Log To Console    \nSending Request to ${GLOBAL_ENDPOINT_CHARGER_DISCONNECT_AC}\n
    DISCONNECT VEHICLE    endpoint=${GLOBAL_ENDPOINT_CHARGER_DISCONNECT_AC}    schema=${GLOBAL_SCHEMA_CHARGER_DISCONNECT_VEHICLE}



    