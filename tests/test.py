import pyttm.libs.crypto as crypto
import unittest

class TestEncryptionFunctions(unittest.TestCase):

    def test_encrypt_text(self):
        text = "Hello, World!"
        secret_key = "mysecretkey"     
        encrypted_text = crypto.encrypt_text(text, secret_key)
        decrypted_text = crypto.decrypt_text(encrypted_text, secret_key)
        self.assertEqual(decrypted_text, text)

    def test_decrypt_text(self):
        text = "Hello, World!"
        secret_key = "mysecretkey"
        encrypted_text = crypto.encrypt_text(text, secret_key)
        decrypted_text = crypto.decrypt_text(encrypted_text, secret_key)
        self.assertEqual(decrypted_text, text)

    def test_hash_password(self):
        password = "mysecretpassword"
        hashed_password = crypto.hash_password(password)
        self.assertNotEqual(hashed_password, "")

    def test_validate_password(self):
        password = "mysecretpassword"
        hashed_password = crypto.hash_password(password)
        self.assertTrue(crypto.validate_password(password, hashed_password))
        self.assertFalse(crypto.validate_password("wrongpassword", hashed_password))

if __name__ == '__main__':
    unittest.main()






