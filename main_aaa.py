from get_aaa_users_info import get_aaa_users_info
from get_credentials import credentials
from get_list_router import get_list_router
from pprint import pprint
import sys
import csv
import signal
import netmiko
import datetime
import time



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
    print("please entre a valide csv file!")
    exit()


# handeling error
auth_error = netmiko.exceptions.NetmikoAuthenticationException
timeout_error = netmiko.exceptions.NetmikoTimeoutException

# storing errors
list_errors = list()

# get username and password from the user
username, password = credentials()


#-------------------- Command aaa ------------------------------
COMMAND_LINE = "display current-configuration configuration aaa"
#---------------------------------------------------------------


def main_aaa():
    # store list of Router with thier users info
    list_aaa_user_info = list()

    for device in router_list:
        try:
            print(f"\n|------ connecting to {device['RouterName']}, {device['IPAddress']} ... ", end="")
            # connect to router via ssh
            connection = netmiko.ConnectHandler(ip=device["IPAddress"], device_type="huawei",username=username,password=password)
            output = connection.send_command(COMMAND_LINE)
            
            # call function to parse the output to dict
            users_info = get_aaa_users_info(output=output,router_name=connection.base_prompt)

            # store each Router user in list
            list_aaa_user_info.append(users_info)

            connection.disconnect()
            print("Done.\n")
        # authentication error
        except auth_error:
            print("Failed.\n")
            print(f"===>> Authentication Failed to {device['RouterName']}, {device['IPAddress']}\n")
            list_errors.append(f"{device['RouterName']},{device['IPAddress']},Authentication Failed\n")
        except timeout_error:
            print("Failed.\n")
            print(f"===>> Connection Timeout to {device['RouterName']}, {device['IPAddress']}\n")
            list_errors.append(f"{device['RouterName']},{device['IPAddress']},Connection Timeout")
    # list of each router with its own users and info
    return list_aaa_user_info

# pprint(main_aaa())

router_aaa_users = main_aaa()

#--------------------------- export user aaa to csv file -----------------
if router_aaa_users != []:
    with open(f"Report_AAA_{current_date}_{current_time}.csv", "w") as report:
        report.write("RouterName\tUserName\tPassword\tServiceType\tLevel\n")
        # write to csv file
        for routers_list in router_aaa_users:
            for router in routers_list.values():
                for user in router.keys():
                    report.write(f"{router[user]['Hostname']}\t{router[user]['Username']}\t{router[user]['Password']}\t{router[user]['Service-type']}\t{router[user]['Level']}\n")
#-------------------------------------------------------------------------

#--------------------------- export errors to csv file -------------------
if list_errors != []:
    with open(f"log_errors_{current_date}_{current_time}.csv", "w") as f_error:
        f_error.write("RouterName,IPAddress,ERROR\n")
        for error in list_errors:
            f_error.write(error)

#-------------------------------------------------------------------------