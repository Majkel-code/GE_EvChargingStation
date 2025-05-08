*** Settings ***
Library    ../lib/percent_generator.py

*** Keywords ***
Generate Random Percent
    [Arguments]    ${min}
    ${random_percent}    Random Percent    ${min}
    RETURN    ${random_percent}
