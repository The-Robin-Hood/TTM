import os
import urllib.parse

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
