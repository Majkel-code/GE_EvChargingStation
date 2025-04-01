*** Settings ***
Resource    ../../../../../testdata/variables/imports.resource
Resource    ../../../../../keywords/imports.resource
Resource    ../charger_keywords/charger_requests.robot



Suite Setup    SETUP CONNECT VEHICLE    ${GLOBAL_ENDPOINT_CHARGER_CONNECT_AC}
Suite Teardown    SETUP DISCONNECT VEHICLE    ${GLOBAL_ENDPOINT_CHARGER_DISCONNECT_AC}

Library    RequestsLibrary

*** Test Cases ***
Verify VEHICLE AC IS CONNECTED
    Log To Console    \nSending Request to ${GLOBAL_ENDPOINT_CHARGER_CONNECT_AC}\n
    ${response}    POST    url=${GLOBAL_ENDPOINT_CHARGER_CONNECT_AC}    expected_status=406
    Validate Schema    inputJson=${response.json()}    referenceSchemaPath=${GLOBAL_SCHEMA_CHARGER_ACTUAL_CONNECTED}
