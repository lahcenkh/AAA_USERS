from getpass import getpass

#------------ geting username and password -------------------------------------
def credentials():
    i = 0
    while i < 3:
        username = input("|-- Entre your Userame: ")
        if username.strip() != '':
            password = getpass(prompt="|-- Entre your Password: ") 
            break
        i += 1
        if i == 3:
            exit()
    return username, password

#-------------------------------------------------------------------------------