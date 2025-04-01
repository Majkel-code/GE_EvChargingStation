*** Settings ***
Resource    ../../../../../testdata/variables/imports.resource
Resource    ../../../../../keywords/imports.resource
Resource    ../charger_keywords/charger_requests.robot

Library    RequestsLibrary

Suite Teardown    SETUP DISCONNECT VEHICLE    ${GLOBAL_ENDPOINT_CHARGER_DISCONNECT_AC}

*** Test Cases ***
Verify VEHICLE AC get all
    Log To Console    \nSending Request to ${GLOBAL_ENDPOINT_CHARGER_CONNECT_AC}\n
    CONNECT VEHICLE    endpoint=${GLOBAL_ENDPOINT_CHARGER_CONNECT_AC}    schema=${GLOBAL_SCHEMA_CHARGER_CONNECT_VEHICLE}



    