*** Settings ***
Resource    ../../../../../testdata/variables/imports.resource
Resource    ../../../../../keywords/imports.resource

Library    RequestsLibrary

*** Keywords ***
VEHICLE get all
    [Arguments]    ${endpoint}    ${schema}
    ${params}    Create Dictionary    filter=all
    ${response}    GET    url=${endpoint}    expected_status=200
    Validate Schema    inputJson=${response.json()}    referenceSchemaPath=${schema}

VEHICLE get specific
    [Arguments]    ${endpoint}    ${schema}    ${option}
    ${response}    GET    url=${endpoint}/${option}    expected_status=200
    Validate Schema    inputJson=${response.json()}    referenceSchemaPath=${schema}

VEHICLE get specific negative
    [Arguments]    ${endpoint}    ${schema}
    ${response}    GET    url=${endpoint}    expected_status=404
    Validate Schema    inputJson=${response.json()}    referenceSchemaPath=${schema}
