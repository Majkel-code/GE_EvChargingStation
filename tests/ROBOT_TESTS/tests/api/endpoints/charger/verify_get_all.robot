*** Settings ***
Resource    ../../../../testdata/variables/imports.resource
Resource    ../../../../keywords/imports.resource

Library    RequestsLibrary

*** Test Cases ***
Verify Existing User
    Log To Console    \nSending Request to ${GLOBAL_ENDPOINT_CHARGER_GET_ALL}\n
    ${params}    Create Dictionary    filter=all
    ${response}    GET    url=${GLOBAL_ENDPOINT_CHARGER_GET_ALL}    expected_status=200
    Validate Schema    inputJson=${response.json()}    referenceSchemaPath=${GLOBAL_SCHEMA_CHARGER_GET_ALL}



    