*** Settings ***
Resource    ../../../../../testdata/variables/imports.resource
Resource    ../../../../../keywords/imports.resource
Resource    ../vehicle_keywords/vehicle_requests.robot

Library    RequestsLibrary

*** Test Cases ***
Verify VEHICLE AC get all
    Log To Console    \nSending Request to ${GLOBAL_ENDPOINT_VEHICLE_AC_GET_ALL}\n
    VEHICLE get all    endpoint=${GLOBAL_ENDPOINT_VEHICLE_AC_GET_ALL}    schema=${GLOBAL_SCHEMA_VEHICLE_AC_GET_ALL}
    # ${params}    Create Dictionary    filter=all
    # ${response}    GET    url=${GLOBAL_ENDPOINT_VEHICLE_AC_GET_ALL}    expected_status=200
    # Validate Schema    inputJson=${response.json()}    referenceSchemaPath=${GLOBAL_SCHEMA_VEHICLE_AC_GET_ALL}



    