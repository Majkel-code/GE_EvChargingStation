*** Settings ***
Resource    ../../../../testdata/variables/imports.resource
Resource    ../../../../keywords/imports.resource

Library    RequestsLibrary

*** Test Cases ***
Verify charger server is alive
    Log To Console    \nSending Request to ${GLOBAL_ENDPOINT_CHARGER_SERVER_ALIVE}\n
    ${params}    Create Dictionary    filter=all
    ${authorization_headers}    Create Dictionary    Authorization=${GLOBAL_AUTH_KEY}
    ${response}    GET    url=${GLOBAL_ENDPOINT_CHARGER_SERVER_ALIVE}    headers=${authorization_headers}    expected_status=200
    Validate Schema    inputJson=${response.json()}    referenceSchemaPath=${GLOBAL_SCHEMA_CHARGER_SERVER_ALIVE}

