from get_aaa_users_info import get_aaa_users_info
from get_credentials import credentials
from get_list_router import get_list_router
from pprint import pprint
from tabulate import tabulate
import sys
import csv
import signal
import netmiko
import datetime
import time
import json


# get date and time
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t).replace(":", "-")
current_date = datetime.date.today()

# handle ctrl + c entreption
signal.signal(signal.SIGINT, signal.SIG_DFL)

# get list of router from csv file
# Note file name is passed throught aregment command line
try:
    router_list = get_list_router(sys.argv[1])
except IndexError:
    print("\n===>> Please entre a valide csv file!\n")
    exit()

# connction type to use to connect to routers telnet or ssh
i = 0
while i < 3:
    connection_type = str(
        input("\n|-- connection type, choose Telnet or SSH: "))
    if connection_type.lower() == "Telnet".lower() or connection_type.lower() == "SSH".lower():
        break
    else:
        print(
            "\n\033[91m ====>> Typing ERROR: Please type SSH or Telnet! \033[0m")
        i += 1

    if i == 3:
        exit()


# handeling error for ssh
auth_error = netmiko.exceptions.NetmikoAuthenticationException
timeout_error = netmiko.exceptions.NetmikoTimeoutException

# storing errors
list_errors = list()

# get username and password from the user
username, password = credentials()

#templet to parse the output
template = "dis_aaa_user.textfsm"

# -------------------- Command aaa ------------------------------
COMMAND_LINE = "display current-configuration configuration aaa"
# ---------------------------------------------------------------


def main_aaa():
    # store list of Router with thier users info
    list_aaa_user_info = list()

    for device in router_list:
        try:
            # connect to router via ssh or telnet
            # this code is add after a change on the source code of netmiko
            if connection_type.lower() == "SSH".lower():
                print(
                    f"\n|------ connecting to {device['RouterName']}, {device['IPAddress']} ...", end="")
                connection = netmiko.ConnectHandler(
                    ip=device["IPAddress"], device_type="huawei", username=username, password=password)
            elif connection_type.lower() == "Telnet".lower():
                print(
                    f"\n|------ connecting to {device['RouterName']}, {device['IPAddress']} ...", end="")
                connection = netmiko.ConnectHandler(
                    ip=device["IPAddress"], device_type="huawei_telnet", username=username, password=password)

            # store command output to parse
            output = connection.send_command(COMMAND_LINE,use_textfsm=True,textfsm_template=template)
            
            for host in output:
                host["host"] = connection.base_prompt

            connection.disconnect()
            print('\033[92m' + "Done.\n" + '\033[0m')
        # handling connection error for ssh
        except auth_error:
            print('\033[91m' + "Failed.\n" + '\033[0m')
            print(
                f"\033[91m \n===>> Authentication Failed to {device['RouterName']}, {device['IPAddress']} \033[0m\n")
            list_errors.append(
                f"{device['RouterName']},{device['IPAddress']},Authentication Failed\n")
        except timeout_error:
            print('\033[91m' + "Failed." + '\033[0m')
            print(
                f"\033[91m \n===>> Connection Timeout to {device['RouterName']}, {device['IPAddress']} \033[0m \n")
            list_errors.append(
                f"{device['RouterName']},{device['IPAddress']},Connection Timeout\n")
        # handling connection error for telnet
        except netmiko.exceptions.ReadTimeout:
            print("Failed.\n")
            print(
                f"\033[91m \n===>> Authentication Failed to {device['RouterName']}, {device['IPAddress']} \033[0m\n")
            list_errors.append(
                f"{device['RouterName']},{device['IPAddress']},Authentication Failed\n")
        except ConnectionResetError:
            print('\033[91m' + "Failed." + '\033[0m')
            print(
                f"\n===>> Connectio Reset to {device['RouterName']}, {device['IPAddress']}\n")
            list_errors.append(
                f"{device['RouterName']},{device['IPAddress']},Authentication Failed\n")
        except TimeoutError:
            print('\033[91m' + "Failed." + '\033[0m')
            print(
                f"\n===>> Connection Timeout to {device['RouterName']}, {device['IPAddress']}\n")
            list_errors.append(
                f"{device['RouterName']},{device['IPAddress']},Connection Timeout\n")

    # list of each router with its own users and info
    return output


# store users in var to export to csv & json file
router_aaa_users = main_aaa()

print(tabulate(router_aaa_users, headers="keys"))