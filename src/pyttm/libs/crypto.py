import os
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def encrypt_text(text: str, secret_key: str):
    secret_key = secret_key.zfill(16).encode('utf-8')
    nonce = os.urandom(16)
    cipher = Cipher(algorithms.AES(secret_key), modes.CTR(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_text = encryptor.update(text.encode('utf-8')) + encryptor.finalize()
    return nonce.hex() + encrypted_text.hex()

def decrypt_text(encrypted_text, secret_key):
    nonce = bytes.fromhex(encrypted_text[:32])
    encrypted_bytes = bytes.fromhex(encrypted_text[32:])
    secret_key = secret_key.zfill(16).encode('utf-8')
    cipher = Cipher(algorithms.AES(secret_key), modes.CTR(nonce), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_bytes = decryptor.update(encrypted_bytes) + decryptor.finalize()
    return decrypted_bytes.decode('utf-8')


def hash_password(password):
    password_bytes = password.encode('utf-8')
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password_bytes)
    hashed_password = sha256_hash.hexdigest()
    return hashed_password


def validate_password(password, hash):
    return hash_password(password) == hash