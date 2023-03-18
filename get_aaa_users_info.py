import re

#----------------------- format the aaa output into dictionary -----------------------------------------------
def get_aaa_users_info(output,router_name):
    # splite the output
    parse_output = output.splitlines()
    # store users
    user_aaa_dict = dict()

    # check if router name key is exist
    if router_name not in user_aaa_dict.keys():
            user_aaa_dict[router_name] = {}
    
    # get user info from the output
    for line in parse_output:
            if re.findall(r"^ local-user \w+ password", line):
                user_name = line.split(" ")
                user_aaa_dict[router_name][user_name[2]] = {
                        "Hostname": router_name,
                        "Username": user_name[2],
                        "Password": user_name[5],
                        "Level": None
                    }
            if re.findall(r"^ local-user \w+ service-type", line):
                user_srv = line.split(" ")
                user_aaa_dict[router_name][user_srv[2]]["Service-type"] = " ".join(user_srv[4:])

            if re.findall(r"^ local-user \w+ level", line):
                user_level = line.split(" ")
                user_aaa_dict[router_name][user_srv[2]]["Level"] = user_level[4]
                
    return user_aaa_dict
#-----------------------------------------------------------------------------------------------------------------