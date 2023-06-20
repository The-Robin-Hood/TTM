import os
import urllib.parse
from time import sleep
from pyttm.libs.crypto import *
from pyttm.libs.totp import TOTPGenerator
from pyttm.libs.db import json_db

def get_password():
    password = json_db.get_password()
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
        json_db.set_password(hash_password(password))
    else :
        while True:
            password = input("Enter password: ")
            if validate_password(password,json_db.get_password()):
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
    json_db.add_creds(totp_info,password)
    print("\nAdded Successfully!")

def list_creds(password):
    while True:
        clear()
        creds = json_db.get_creds(password)
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
    creds = json_db.get_creds(password)
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
            json_db.delete_creds(choice-1)
            print("Deleted Successfully!")
        else:
            print("Aborted!")
            exit()

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    display_banner()

def display_banner():
    print("""
 -------------------------- 
|  _____   _____   __  __  |
| |_   _| |_   _| |  \/  | |
|   | |     | |   | |\/| | |
|   | |     | |   | |  | | |
|   |_|     |_|   |_|  |_| |
|                          |  
|   Terminal TOTP Manager  |
|      version : 0.0.3     |
 --------------------------
""")    

def extract_info_from_otpauth_uri(uri):
    parsed_uri = urllib.parse.urlparse(uri)

    if parsed_uri.scheme != "otpauth" or parsed_uri.netloc != "totp":
        raise ValueError("Invalid OTPAuth URI")

    label = parsed_uri.path.strip('/')
    query_params = urllib.parse.parse_qs(parsed_uri.query)


    if 'secret' not in query_params:
        raise ValueError("Secret parameter not found in OTPAuth URI")

    secret = query_params['secret'][0]
    algorithm = query_params['algorithm'][0] if 'algorithm' in query_params else 'sha1'
    digits = query_params['digits'][0] if 'digits' in query_params else 6
    period = query_params['period'][0] if 'period' in query_params else 30
    label = query_params['issuer'][0]+" "+label if 'issuer' in query_params else label

    return {'issuer': label, 'seed': secret, 'algorithm': algorithm, 'digits': digits, 'period': period}

def gather_info_from_user():
    issuer = input("Enter issuer: ")
    seed = input("Enter seed: ")
    algorithm = input("Enter algorithm (Default: sha1): ")
    digits = input("Enter digits (Default: 6): ")
    period = input("Enter period (Default: 30): ")
    if algorithm == "":
        algorithm = "sha1"
    if digits == "":
        digits = 6
    if period == "":
        period = 30
    return {
        "issuer": issuer,
        "seed": seed,
        "algorithm": algorithm,
        "digits": digits,
        "period": period
    }