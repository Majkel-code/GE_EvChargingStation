*** Settings ***
Resource    ../../../../testdata/variables/imports.resource
Resource    ../../../../keywords/imports.resource

Library    RequestsLibrary

*** Test Cases ***
Verify Existing User
    Log To Console    \nSending Request to ${GLOBAL_ENDPOINT_CHARGER_GET_SPECIFIC_NEGATIVE}\n
    ${params}    Create Dictionary    filter=all
    ${response}    GET    url=${GLOBAL_ENDPOINT_CHARGER_GET_SPECIFIC_NEGATIVE}    expected_status=404
    Validate Schema    inputJson=${response.json()}    referenceSchemaPath=${GLOBAL_SCHEMA_CHARGER_GET_SPECIFIC_NEGATIVE}

