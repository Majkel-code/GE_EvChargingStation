*** Settings ***
Resource    ../../../../../testdata/variables/imports.resource
Resource    ../../../../../keywords/imports.resource
Resource    ../charger_keywords/charger_requests.robot

Library    RequestsLibrary
Library    ../../../../../../../.venv/lib/python3.12/site-packages/robot/libraries/Process.py

Suite Setup    SETUP CONNECT VEHICLE    ${GLOBAL_ENDPOINT_CHARGER_CONNECT_CHADEMO}
Suite Teardown    SETUP DISCONNECT VEHICLE    ${GLOBAL_ENDPOINT_CHARGER_DISCONNECT_CHADEMO}


*** Test Cases ***
Verify VEHICLE CHADEMO charge to Above 100%
    Log To Console    \nSending Request to ${GLOBAL_ENDPOINT_CHARGER_CHARGE_SESSION_CHADEMO_CUSTOM_PERCENT}${GLOBAL_CHADEMO_PERCENT_200}\n
    ${response}    POST    url=${GLOBAL_ENDPOINT_CHARGER_CHARGE_SESSION_CHADEMO_CUSTOM_PERCENT}${GLOBAL_CHADEMO_PERCENT_200}    expected_status=406
    Validate Schema    inputJson=${response.json()}    referenceSchemaPath=${GLOBAL_SCHEMA_CHARGER_SESSION_ABOVE_LIMIT}
    ${error_message}    Get From Dictionary    ${response.json()}    error
    Should Be Equal As Strings    ${error_message}    UNABLE TO PERFORM CHARGE SESSION - PERCENT SHOULD BE 100 OR LOWER!
        
