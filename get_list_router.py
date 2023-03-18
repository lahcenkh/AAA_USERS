import csv
#------------------------ list of router in csv file ---------------------------
def get_list_router(filename):
# get file name from argement command line
        # path of list of routers
    file_path_routers = filename
    if file_path_routers.endswith(".csv"):
        pass


    # hold list of routers in list
    router_list = list()

    with open(file_path_routers, "r") as router_f:
        r = csv.reader(router_f)
        next(r)
        for dev in r:
            # create dict() and append it to router_list var
            router_list.append({"RouterName": dev[0], "IPAddress": dev[1]})
    
    return router_list
#-------------------------------------------------------------------------------