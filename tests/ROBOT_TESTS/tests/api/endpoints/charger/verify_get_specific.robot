*** Settings ***
Resource    ../../../../testdata/variables/imports.resource
Resource    ../../../../keywords/imports.resource

Library    RequestsLibrary

Test Template    Custom Test Template

*** Test Cases ***                                OPTION
Verify CHARGING_OUTLETS                           CHARGING_OUTLETS    
Verify MAX_CHARGING_POWER_CHADEMO                 MAX_CHARGING_POWER_CHADEMO
Verify MAX_CHARGING_POWER_AC                      MAX_CHARGING_POWER_AC
Verify AC_ACTUAL_KW_PER_MIN                       AC_ACTUAL_KW_PER_MIN
Verify CHADEMO_ACTUAL_KW_PER_MIN                  CHADEMO_ACTUAL_KW_PER_MIN
Verify MAX_CHARGING_AMPERE                        MAX_CHARGING_AMPERE
Verify VOLT                                       VOLT
Verify LOSSES_DURING_CHARGING                     LOSSES_DURING_CHARGING
Verify VOLTAGE_DROP_AC                            VOLTAGE_DROP_AC
Verify VOLTAGE_DROP_CHADEMO                       VOLTAGE_DROP_CHADEMO


*** Keywords ***
Custom Test Template
    [Arguments]    ${option}
    Log To Console    \nSending Request to ${GLOBAL_ENDPOINT_CHARGER_GET_SPECIFIC}/${option}\n
    ${response}    GET    url=${GLOBAL_ENDPOINT_CHARGER_GET_SPECIFIC}/${option}    expected_status=200
    Validate Schema    inputJson=${response.json()}    referenceSchemaPath=${GLOBAL_SCHEMA_CHARGER_GET_SPECIFIC}