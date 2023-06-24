import os
from getpass import getpass
import sys
from typing import Final
import urllib.parse
import requests
import pkg_resources
from time import sleep
from datetime import datetime
from pyttm.libs.db import SQLiteDB
import pyttm.libs.crypto as crypto
from pyttm.libs.totp import TOTPGenerator
from pyttm import __version__ as ver
ConfigDB: Final = SQLiteDB()

def get_password():
    password_hash = ConfigDB.password_hash
    if not password_hash:
        print("Welcome to TOTP Manager!\n")
        print("Create a password to secure your credentials.")
        while True:
            password = getpass("\nPassword: ")
            if (len(password) < 8):
                clear()
                print("Password must be at least 8 characters!")
                continue
            confirm_password = getpass("Confirm password: ")
            if password == confirm_password:
                break
            else:
                clear()
                print("Password does not match!")
        ConfigDB.password_hash = crypto.hash_password(password)
    else:
        while True:
            password = getpass("Enter password: ")
            if crypto.validate_password(password, ConfigDB.password_hash):
                break
            else:
                clear()
                print("Invalid password!")
    return password


def add_creds(password):
    if (input("Do you have otpauth uri? (y/n): ") in ["y", "Y"]):
        link = input("Enter otpauth link: ")
        totp_info = extract_info_from_otpauth_uri(link)
    else:
        totp_info = gather_info_from_user()
    
    ConfigDB.add_creds(totp_info, password)
    print("\nAdded Successfully!")


def list_creds(password):
    while True:
        clear()
        creds = ConfigDB.get_creds(password)
        
        if not len(creds):
            print("No Credentials Found!")
            if (input("Do you want to add? (y/n): ") in ["y", "Y"]):
                add_creds(password)
                break
            sys.exit()
        
        max_key_length = max(len(cred["issuer"]) for cred in creds)
        
        print(f"Issuer{' '*(max_key_length-5)}    OTP     Time")
        print("-"*(max_key_length+19))
        
        for cred in creds:
            i = TOTPGenerator(**cred)
            padding = ' ' * (max_key_length - len(cred["issuer"]))
            print(
                f"{cred['issuer']}{padding}    {i.generateTOTP()}    {i.get_remaining_time()}")
        
        print("\n\nPress Ctrl+C to exit")
        sleep(1)
        print("\n")


def delete_creds(password):
    clear()
    creds = ConfigDB.get_creds(password)
    if len(creds) == 0:
        print("No Credentials Found!")
        if (input("Do you want to add? (y/n): ") in ["y", "Y"]):
            add_creds(password)
        sys.exit()
    else:
        print(f'Issuer\n{"-" * 6}')
        for index, cred in enumerate(creds):
            print(f"{index + 1}. {cred['issuer']}")
        choice = int(input("\nChoose the Issuer to delete: "))
        if choice > len(creds) or choice < 1:
            print("Invalid choice!")
            sys.exit()
        if (input(f"Are you sure you want to delete {creds[choice-1]['issuer']}? (y/n): ") in ["y", "Y"]):
            ConfigDB.delete_cred(choice)
            print("Deleted Successfully!")
        else:
            print("Aborted!")
            sys.exit()


def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    display_banner()


def display_banner():
    print(f"""
 -------------------------- 
|  _____   _____   __  __  |
| |_   _| |_   _| |  \/  | |
|   | |     | |   | |\/| | |
|   | |     | |   | |  | | |
|   |_|     |_|   |_|  |_| |
|                          |  
|   Terminal TOTP Manager  |
|      version : {ver}     |
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
    label = f'{query_params["issuer"][0]} {label}' if 'issuer' in query_params else label

    return {'issuer': label, 'seed': secret, 'algorithm': algorithm, 'digits': digits, 'period': period}


def gather_info_from_user():
    issuer = input("Enter Issuer: ")
    seed = input("Enter Secret Key: ")
    algorithm = input("Enter Algorithm (Default: sha1): ")
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

def check_for_updates():
    last_checked = ConfigDB.get_last_check()
    if last_checked:
        if (datetime.now() - datetime.strptime(last_checked, "%Y-%m-%d %H:%M:%S.%f")).days < 1:
            return
    ConfigDB.set_last_check(datetime.now())
    try:
        fetch = requests.get("https://pypi.org/pypi/pyttm/json")
        latest_version = fetch.json()["info"]["version"]
        if latest_version != ver :
            print(f"\nUpdate available: {latest_version}")
            print("Run 'pip install --upgrade pyttm\nor\ndownload the latest binary from release' to update\n")
    except:
        pass