from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib


def encrypt_text(text: str, secret_key: str):
    secret_key = secret_key.zfill(16)
    nonce = get_random_bytes(8)
    secret_key_to_bytes = secret_key.encode('utf-8')
    cipher = AES.new(secret_key_to_bytes, AES.MODE_CTR, nonce=nonce)
    encrypted_text = cipher.encrypt(text.encode('utf-8'))
    return nonce.hex() + encrypted_text.hex()


def decrypt_text(encrypted_text, secret_key):
    nonce = bytes.fromhex(encrypted_text[:16])
    secret_key = secret_key.zfill(16)
    encrypted_bytes = bytes.fromhex(encrypted_text[16:])
    secret_key_to_bytes = secret_key.encode('utf-8')
    cipher = AES.new(secret_key_to_bytes, AES.MODE_CTR, nonce=nonce)
    decrypted_text = cipher.decrypt(encrypted_bytes)
    return decrypted_text.decode('utf-8')


def hash_password(password):
    password_bytes = password.encode('utf-8')
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password_bytes)
    hashed_password = sha256_hash.hexdigest()
    return hashed_password


def validate_password(password, hash):
    return hash_password(password) == hash
