import time
import requests

def check_charger_data(url_charger, auth_key):
    time.sleep(1)
    url = f"{url_charger}"
    headers = {"Content-Type": "application/json", "Authorization": auth_key}
    response = requests.get(url, headers=headers)
    if response.ok:
        return response


# def wait_for_sessions_end(charger_endpoint, connector :list, auth_key):
#     timeout_iteration = 0
#     while timeout_iteration < 30:
#         if "AC" and "CHADEMO" in connector:
#             first_check_ac = check_charger_data(url_charger=f"{charger_endpoint}/ac_charging_ongoing", auth_key=auth_key).json()
#             first_check_chademo = check_charger_data(url_charger=f"{charger_endpoint}/chademo_charging_ongoing", auth_key=auth_key).json()
#             time.sleep(1)
#             second_check_ac = check_charger_data(url_charger=f"{charger_endpoint}/ac_charging_ongoing", auth_key=auth_key).json()
#             second_check_chademo = check_charger_data(url_charger=f"{charger_endpoint}/chademo_charging_ongoing", auth_key=auth_key).json()
#         elif "AC" in connector:
#             first_check_ac = check_charger_data(url_charger=f"{charger_endpoint}/ac_charging_ongoing", auth_key=auth_key).json()
#             time.sleep(1)
#             second_check_ac = check_charger_data(url_charger=f"{charger_endpoint}/ac_charging_ongoing", auth_key=auth_key).json()
#         elif "CHADEMO" in connector:
#             first_check_chademo = check_charger_data(url_charger=f"{charger_endpoint}/chademo_charging_ongoing", auth_key=auth_key).json()
#             time.sleep(1)
#             second_check_chademo = check_charger_data(url_charger=f"{charger_endpoint}/chademo_charging_ongoing", auth_key=auth_key).json()

#         if "AC" and "CHADEMO" in connector:
#             if first_check_ac["data"]["ac_charging_ongoing"] == second_check_ac["data"]["ac_charging_ongoing"] \
#                     or first_check_chademo["data"]["chademo_charging_ongoing"] == second_check_chademo["data"]["chademo_charging_ongoing"]:
#                 if check_charger_data(url_charger=f"{charger_endpoint}/ac_finished", auth_key=auth_key).json()["data"]["ac_finished"]:
#                     timeout_iteration = 0
#                     print("AC FINISHED BUGGGGGGGGG")
#                 else:
#                     timeout_iteration += 1
#                     print("TIMEOUT ITERATION: AC/CHADEMO", timeout_iteration)
#         elif "AC" in connector:
#             if first_check_ac["data"]["ac_charging_ongoing"] == second_check_ac["data"]["ac_charging_ongoing"]:
#                 if check_charger_data(url_charger=f"{charger_endpoint}/ac_finished", auth_key=auth_key).json()["data"]["ac_finished"]:
#                     timeout_iteration = 0

#                 else:
#                     timeout_iteration += 1
#                     print("TIMEOUT ITERATION: AC", timeout_iteration)
#         elif "CHADEMO" in connector:
#             if first_check_chademo["data"]["chademo_charging_ongoing"] == second_check_chademo["data"]["chademo_charging_ongoing"]:
#                 if check_charger_data(url_charger=f"{charger_endpoint}/chademo_finished", auth_key=auth_key).json()["data"]["chademo_finished"]:
#                     timeout_iteration = 0

#                 else:
#                     timeout_iteration += 1
#                     print("TIMEOUT ITERATION: CHADEMO", timeout_iteration)



def wait_for_chademo_end(charger_endpoint, connector, auth_key):
    timeout_iteration = 0
    while timeout_iteration < 30:
        if "CHADEMO" == connector:
            first_check_chademo = check_charger_data(url_charger=f"{charger_endpoint}/chademo_charging_ongoing", auth_key=auth_key).json()
            time.sleep(1)
            second_check_chademo = check_charger_data(url_charger=f"{charger_endpoint}/chademo_charging_ongoing", auth_key=auth_key).json()
            if first_check_chademo["data"]["chademo_charging_ongoing"] == second_check_chademo["data"]["chademo_charging_ongoing"]:
                if check_charger_data(url_charger=f"{charger_endpoint}/chademo_finished", auth_key=auth_key).json()["data"]["chademo_finished"]:
                    timeout_iteration = 0
                    return True
                else:
                    timeout_iteration += 1


def wait_for_ac_end(charger_endpoint, connector, auth_key):
    timeout_iteration = 0
    while timeout_iteration < 30:
        if "AC" == connector:
            first_check_ac = check_charger_data(url_charger=f"{charger_endpoint}/ac_charging_ongoing", auth_key=auth_key).json()
            time.sleep(1)
            second_check_ac = check_charger_data(url_charger=f"{charger_endpoint}/ac_charging_ongoing", auth_key=auth_key).json()
            if first_check_ac["data"]["ac_charging_ongoing"] == second_check_ac["data"]["ac_charging_ongoing"]:
                if check_charger_data(url_charger=f"{charger_endpoint}/ac_finished", auth_key=auth_key).json()["data"]["ac_finished"]:
                    timeout_iteration = 0
                    return True
                else:
                    timeout_iteration += 1
                    print("TIMEOUT ITERATION AC: ", timeout_iteration)