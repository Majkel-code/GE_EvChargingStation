*** Settings ***
Library    ../lib/energy_ongoing_timeout.py

*** Keywords ***
# WAIT FOR SESSION END
#     [Arguments]    ${charger_endpoint}    ${connector}    ${auth_key}
#     Log To Console    Wait for session end
#     Log To Console    ${connector}
#     # ${timeout_return}    Ac Timeout    ${charger_endpoint}    ${connector}    ${auth_key}
#     ${timeout_return}    Wait For Sessions End    ${charger_endpoint}    ${connector}    ${auth_key}
#     RETURN    ${timeout_return}

WAIT FOR CHADEMO SESSION END
    [Arguments]    ${charger_endpoint}    ${connector}    ${auth_key}
    Log To Console    Wait for session end
    Log To Console    ${connector}
    ${timeout_return}    Wait For Chademo End    ${charger_endpoint}    ${connector}    ${auth_key}
    RETURN    ${timeout_return}


WAIT FOR AC SESSION END
    [Arguments]    ${charger_endpoint}    ${connector}    ${auth_key}
    Log To Console    Wait for session end
    Log To Console    ${connector}
    ${timeout_return}    Wait For Ac End    ${charger_endpoint}    ${connector}    ${auth_key}
    RETURN    ${timeout_return}


#     ${timeout_return}    Wait For Ac End    ${charger_endpoint}    ${connector}    ${auth_key}
#     RETURN    ${timeout_return}
    
    # WHILE    True
    #     IF    ${timeout}
    #         RETURN    ${timeout}
    #     ELSE
    #         ${timeout}    Custom Timeout Ac    ${charger_endpoint}    ${auth_key}
    #     END
    # END