import os
from pathlib import Path
import sqlite3
from typing import Optional, TypedDict

from pyttm.libs.crypto import decrypt_text, encrypt_text


class Credentials(TypedDict):
    issuer: str
    seed: str
    algorithm: str
    digits: int
    period: int


class SQLiteDB:
    def __init__(self):
        self.create_table()

    @property
    def ttm_dir(self):
        if os.name == 'nt':
            config_dir = os.environ.get(
                'APPDATA', Path.home().joinpath('AppData', 'Roaming'))

        elif os.name == 'posix':
            config_dir = os.environ.get(
                'XDG_CONFIG_HOME', Path.home().joinpath('.config'))

        else:
            config_dir = Path(__file__).parent.parent

        return Path(config_dir).joinpath('ttm')

    @property
    def config_db(self):
        os.makedirs(self.ttm_dir, exist_ok=True)
        return Path(self.ttm_dir).joinpath('config.db')

    def create_table(self):
        with sqlite3.connect(self.config_db) as connection:
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Password (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                password TEXT
            )''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS Credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                issuer TEXT,
                seed TEXT,
                algorithm TEXT,
                digits INTEGER,
                period INTEGER
            )''')

    @property
    def password_hash(self) -> Optional[str]:
        with sqlite3.connect(self.config_db) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT password FROM Password ORDER BY id DESC")
            result = cursor.fetchone()
            if result:
                return result[0]

    @password_hash.setter
    def password_hash(self, password: str):
        with sqlite3.connect(self.config_db) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO Password (password) VALUES (?)", (password,))

    def get_creds(self, password: str):
        with sqlite3.connect(self.config_db) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Credentials")
            rows = cursor.fetchall()
            creds = []
            for row in rows:
                cred = {
                    'issuer': row[1],
                    'seed': decrypt_text(row[2], password),
                    'algorithm': row[3],
                    'digits': row[4],
                    'period': row[5]
                }
                creds.append(cred)
            return creds

    def add_creds(self, creds: Credentials, password: str):
        with sqlite3.connect(self.config_db) as connection:
            cursor = connection.cursor()
            encrypted_seed = encrypt_text(creds['seed'], password)
            cursor.execute("INSERT INTO Credentials (issuer, seed, algorithm, digits, period) VALUES (?, ?, ?, ?, ?)",
                           (creds['issuer'], encrypted_seed, creds['algorithm'], creds['digits'], creds['period']))

    def delete_cred(self, cred_id: int):
        with sqlite3.connect(self.config_db) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Credentials WHERE id=?", (cred_id,))


ConfigDB = SQLiteDB()
