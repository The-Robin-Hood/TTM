import sys
from crypto_utils import *
from utils import *
from db import JsonDB
from totp import TOTPGenerator
from time import sleep

def get_password():
    password = DB.get_password()
    if password == "":
        print("Welcome to TOTP Manager!\n")
        print("Create a password to secure your credentials.")
        while True:
            password = input("\nPassword: ")
            if(len(password) < 8):
                clear()
                print("Password must be at least 8 characters!")
                continue
            confirm_password = input("Confirm password: ")
            if password == confirm_password:
                break
            else:
                clear()
                print("Password does not match!")
        DB.set_password(hash_password(password))
    else :
        while True:
            password = input("Enter password: ")
            if validate_password(password,DB.get_password()):
                break   
            else:
                clear()
                print("Invalid password!")
    return password   

def add_creds(password):
    if(input("Do you have otpauth uri? (y/n): ") in ["y","Y"]):
                link = input("Enter otpauth link: ")
                totp_info = extract_info_from_otpauth_uri(link)
    else:
        totp_info = gather_info_from_user()
    DB.add_creds(totp_info,password)
    print("\nAdded Successfully!")

def list_creds(password):
    while True:
        clear()
        creds = DB.get_creds(password)
        if len(creds) == 0:
            print("No Credentials Found!")
            if(input("Do you want to add? (y/n): ") in ["y","Y"]):
                add_creds(password)
                break
            exit()
        max_key_length = max(len(cred["issuer"]) for cred in creds)
        print("Issuer"+' '*(max_key_length-5)+"    OTP     Time")
        print("-"*(max_key_length+19))
        for cred in creds:
            i = TOTPGenerator(**cred)
            padding = ' ' * (max_key_length - len(cred["issuer"]))
            print(f"{cred['issuer']}{padding}    {i.generateTOTP()}    {i.get_remaining_time()}")
        print("\n\nPress Ctrl+C to exit")
        sleep(1)
        print("\n")

def delete_creds(password):
    clear()
    creds = DB.get_creds(password)
    if len(creds) == 0:
        print("No Credentials Found!")
        if(input("Do you want to add? (y/n): ") in ["y","Y"]):
            add_creds(password)
        exit()
    else:
        print("Issuer"+"\n"+"-"*6)
        for index,cred in enumerate(creds):
            print(f"{index+1}. {cred['issuer']}")
        choice = int(input("\nChoose the Issuer to delete: "))
        if choice > len(creds) or choice < 1:
            print("Invalid choice!")
            exit()
        if(input(f"Are you sure you want to delete {creds[choice-1]['issuer']}? (y/n): ") in ["y","Y"]):
            DB.delete_creds(choice-1)
            print("Deleted Successfully!")
        else:
            print("Aborted!")
            exit()


if __name__ == "__main__": 
    try:
        clear()  
        command_line_args = sys.argv[1:]
        if len(command_line_args) == 0 or command_line_args[0] not in ["add","list","delete"]:
            print("Usage: python3 app.py add|list|delete\n")
            exit()
        
        DB = JsonDB("db.json")
        password = get_password()        
        command = command_line_args[0]

        if command == "add":
            add_creds(password)
        elif command == "list":
            list_creds(password)
        elif command == "delete":
            delete_creds(password)

    except KeyboardInterrupt:
        print("\nExiting...")
        exit()
    except ValueError:
        print("Invalid input!")
        exit()
    except Exception as e:
        print("Error! Facing Issue, Please Report!")
        print(e)
        exit()
