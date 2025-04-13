*** Settings ***
Resource    ../../../../../testdata/variables/imports.resource
Resource    ../../../../../keywords/imports.resource
Resource    ../charger_keywords/charger_requests.robot

Library    RequestsLibrary

Suite Setup    SETUP CONNECT VEHICLE    ${GLOBAL_ENDPOINT_CHARGER_CONNECT_CHADEMO}
Suite Teardown    SETUP DISCONNECT VEHICLE    ${GLOBAL_ENDPOINT_CHARGER_DISCONNECT_CHADEMO}


*** Test Cases ***
Verify VEHICLE CHADEMO charge RANDOM %
    Log To Console    \nSending Request to ${GLOBAL_ENDPOINT_VEHICLE_CHADEMO_BATTERY_LEVEL}\n
    ${response}    GET    url=${GLOBAL_ENDPOINT_VEHICLE_CHADEMO_BATTERY_LEVEL}    expected_status=200
    ${battery_level}    Get From Dictionary    ${response.json()["data"]["parameters"]}    BATTERY_LEVEL
    ${random_percent}    Generate Random Percent    ${battery_level}

    Log To Console    \nSending Request to ${GLOBAL_ENDPOINT_CHARGER_CHARGE_SESSION_CHADEMO_CUSTOM_PERCENT}${random_percent}\n
    ${response}    POST    url=${GLOBAL_ENDPOINT_CHARGER_CHARGE_SESSION_CHADEMO_CUSTOM_PERCENT}${random_percent}    expected_status=200
    ${session_end}    WAIT FOR CHADEMO SESSION END
    ...    ${GLOBAL_API_URL_CHARGER}
    ...    connector=CHADEMO
    ...    auth_key=${GLOBAL_AUTH_KEY}
    IF    ${session_end} == True
        ${authorization_headers}    Create Dictionary    Authorization=${GLOBAL_AUTH_KEY}
        Log To Console    \nSending Request to ${GLOBAL_ENDPOINT_CHARGER_CHADEMO_FINISHED}\n
        ${response_ac_finished}    GET    url=${GLOBAL_ENDPOINT_CHARGER_CHADEMO_FINISHED}    
        ...    headers=${authorization_headers}    expected_status=200
        Validate Schema    ${response_ac_finished.json()}    ${GLOBAL_SCHEMA_CHARGER_SESSION_CHADEMO_FINISHED}
        ${status}    Get From Dictionary    ${response_ac_finished.json()["data"]}     chademo_finished
        Should Be Equal As Strings    ${status}    True
        
        Log To Console     \nSending Request to ${GLOBAL_ENDPOINT_VEHICLE_CHADEMO_BATTERY_LEVEL}\n
        ${response_battery_level}    GET    url=${GLOBAL_ENDPOINT_VEHICLE_CHADEMO_BATTERY_LEVEL}    expected_status=200
        ${battery_level}    Get From Dictionary    ${response_battery_level.json()["data"]["parameters"]}    BATTERY_LEVEL
        Should Be Equal As Numbers    ${battery_level}    ${random_percent}

        Log To Console     \nSending Request to ${GLOBAL_ENDPOINT_VEHICLE_CHADEMO_MAX_BATTERY_CAPACITY_IN_KWH}\n
        ${response_max_battery}    GET    url=${GLOBAL_ENDPOINT_VEHICLE_CHADEMO_MAX_BATTERY_CAPACITY_IN_KWH}    expected_status=200
        ${max_battery}    Get From Dictionary    ${response_max_battery.json()["data"]["parameters"]}    MAX_BATTERY_CAPACITY_IN_KWH
        ${expected_battery_level}    Calculate Expected KW Level    ${random_percent}    ${max_battery}
        Log To Console    Expected Battery Level: ${expected_battery_level}
        
        Log To Console     \nSending Request to ${GLOBAL_ENDPOINT_VEHICLE_CHADEMO_ACTUAL_BATTERY_STATUS_IN_KWH}\n
        ${response_actual_battery}    GET    url=${GLOBAL_ENDPOINT_VEHICLE_CHADEMO_ACTUAL_BATTERY_STATUS_IN_KWH}    expected_status=200
        ${actual_battery}    Get From Dictionary    ${response_actual_battery.json()["data"]["parameters"]}    ACTUAL_BATTERY_STATUS_IN_KWH
        Should Be Equal As Numbers    ${actual_battery}    ${expected_battery_level}
        
    END
        
