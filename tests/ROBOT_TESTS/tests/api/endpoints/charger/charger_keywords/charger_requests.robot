*** Settings ***
Resource    ../../../../../testdata/variables/imports.resource
Resource    ../../../../../keywords/imports.resource

Library    Collections
Library    RequestsLibrary

*** Keywords ***
CONNECT VEHICLE
    [Arguments]    ${endpoint}    ${schema}
    ${params}    Create Dictionary    filter=all
    ${response}    POST    url=${endpoint}    expected_status=200
    Validate Schema    inputJson=${response.json()}    referenceSchemaPath=${schema}

DISCONNECT VEHICLE
    [Arguments]    ${endpoint}    ${schema}
    ${params}    Create Dictionary    filter=all
    ${response}    POST    url=${endpoint}    expected_status=200
    Validate Schema    inputJson=${response.json()}    referenceSchemaPath=${schema}

SETUP CONNECT VEHICLE
    [Arguments]    ${endpoint}
    ${params}    Create Dictionary    filter=all
    ${response}    POST    url=${endpoint}    expected_status=200
    ${connected}    Set Variable    ${response.json()}
    # ${connected_boolean}    Get From Dictionary    ${connected}    response
    # RETURN    ${connected_boolean}

SETUP DISCONNECT VEHICLE
    [Arguments]    ${endpoint}
    ${params}    Create Dictionary    filter=all
    ${response}    POST    url=${endpoint}    expected_status=200
    ${disconnected}    Set Variable    ${response.json()}
    # ${disconnected_boolean}    Get From Dictionary    ${disconnected}    response
    # RETURN    ${disconnected_boolean}


    
# VEHICLE get specific
#     [Arguments]    ${endpoint}    ${schema}    ${option}
#     ${response}    GET    url=${endpoint}/${option}    expected_status=200
#     Validate Schema    inputJson=${response.json()}    referenceSchemaPath=${schema}

# VEHICLE get specific negative
#     [Arguments]    ${endpoint}    ${schema}
#     ${response}    GET    url=${endpoint}    expected_status=404
#     Validate Schema    inputJson=${response.json()}    referenceSchemaPath=${schema}
