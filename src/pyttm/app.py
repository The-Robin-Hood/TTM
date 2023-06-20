# __main__.py

import sys
from pyttm.libs.helper import *
from pyttm.libs.crypto import *

def main():
    try:
        clear()  
        command_line_args = sys.argv[1:]
        if len(command_line_args) == 0 or command_line_args[0] not in ["add","list","delete"]:
            print("Usage: ttm add|list|delete\n")
            exit()

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

if __name__ == "__main__":
    main()
