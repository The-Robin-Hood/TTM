import os
import json
import copy
from crypto_utils import encrypt_text, decrypt_text

class JsonDB:
    def __init__(self, file_path):
        self.file_path = os.path.abspath(file_path)
        self.data = self.read_data()

    def create_file(self):
        with open(self.file_path, 'w') as file:
            json.dump({
                "password": "",
                "credentials": []
            }, file, indent=4)
    
    def read_data(self):
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            self.create_file()
            return self.read_data()

    def write_data(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, indent=4)

    def get_password(self):
        return self.data["password"]
    
    def set_password(self, password):
        self.data["password"] = password
        self.write_data()
    
    def add_creds(self, creds,password):
        secret_key = password.zfill(16)
        creds['seed'] = encrypt_text(creds['seed'], secret_key)
        self.data["credentials"].append(creds)
        self.write_data()
    
    def get_creds(self,password):
        secret_key = password.zfill(16)
        creds = copy.deepcopy(self.data["credentials"])
        for cred in creds:
            cred['seed'] = decrypt_text(cred['seed'], secret_key)
        return creds
    
    def delete_creds(self, cred):
        del self.data["credentials"][cred]
        self.write_data()