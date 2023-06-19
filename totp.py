import base64
import hashlib
import hmac
import time

class TOTPGenerator:
    def __init__(self, seed: str, algorithm: str = "sha1", period: int = 30, digits: int = 6, **kwargs):
        try:
            if algorithm.lower() not in ["sha1", "sha256", "sha512"]:
                raise ValueError("Invalid algorithm. Must be one of 'sha1', 'sha256', or 'sha512'")
            if digits not in [6, 8]:
                raise ValueError("Invalid digits. Must be either 6 or 8")
            if period <= 0:
                raise ValueError("Invalid period. Must be greater than 0")
            if len(seed) % 8 != 0:
                seed = seed + "=" * (8 - len(seed) % 8)

            self.seed = seed
            self.algorithm = algorithm.lower()
            self.period = period
            self.digits = digits

        except ValueError as error:
            print(error)
    
    def generateTOTP(self):
        try:                
            # Decode the seed from base32 to obtain the key
            key = base64.b32decode(self.seed.upper())

            # Get the current time in intervals of given period
            now = int(time.time() // self.period)

            # Convert the current time to a byte string of length 8
            time_in_bytes = now.to_bytes(8, "big")

            # Create an HMAC object using the key and time byte string, with given algorithm
            if self.algorithm == "sha1":
                hashing = hmac.new(key, time_in_bytes, hashlib.sha1)
            elif self.algorithm == "sha256":
                hashing = hmac.new(key, time_in_bytes, hashlib.sha256)
            elif self.algorithm == "sha512":
                hashing = hmac.new(key, time_in_bytes, hashlib.sha512)

            # Calculate the digest of the HMAC object
            digest = hashing.digest()

            # Get the last byte of the digest to extract the offset value
            offset = digest[-1] & 0x0f

            # Extract a 4-byte slice from the digest starting from the calculated offset
            truncated_hash = digest[offset:offset + 4]

            # Convert the truncated hash to an integer using big-endian byte order
            truncated_hash_int = int.from_bytes(truncated_hash, "big")

            # Remove the most significant bit by applying a bitwise AND operation
            truncated_hash_int &= 0x7fffffff

            if self.digits == 8:
                otp = truncated_hash_int % 100000000
            elif self.digits == 6:
                otp = truncated_hash_int % 1000000
            
            # Convert the OTP to a string
            totp = str(otp).zfill(self.digits)

            # Return the generated 6-digit OTP
            return totp
        
        except Exception as err:
            print(err)
            return None

    def get_remaining_time(self):
        return self.period - int(time.time() % self.period)