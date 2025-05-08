*** Settings ***
Resource    ../../../../testdata/variables/imports.resource
Resource    ../../../../keywords/imports.resource

Library    RequestsLibrary

*** Test Cases ***
Verify negative authorization
    Log To Console    \nSending Request to ${GLOBAL_ENDPOINT_CHARGER_UNABLE_AUTHORIZATION}\n
    ${params}    Create Dictionary    filter=all
    ${response}    GET    url=${GLOBAL_ENDPOINT_CHARGER_UNABLE_AUTHORIZATION}    expected_status=200
    Validate Schema    inputJson=${response.json()}    referenceSchemaPath=${GLOBAL_SCHEMA_CHARGER_UNABLE_AUTHORIZED}

