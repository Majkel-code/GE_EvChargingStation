*** Settings ***
Library    ../lib/charge_session_calculator.py

*** Keywords ***
Calculate Expected KW Level
    [Arguments]    ${percent}    ${max_capacity}
    ${expected_kw}    Calculate Expected Kw    ${percent}    ${max_capacity}
    RETURN    ${expected_kw}
