"""
RNCryptor-compatible decryption for template files.
Based on RNCryptor data format v3 specification.
"""

import hashlib
import hmac
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2


class RNCryptorDecryptor:
    """Decrypts data encrypted with RNCryptor (version 3)"""
    
    PBKDF2_ITERATIONS = 10000
    PBKDF2_KEY_SIZE = 32
    PBKDF2_SALT_SIZE = 8
    AES_KEY_SIZE = 32
    HMAC_KEY_SIZE = 32
    IV_SIZE = 16
    
    def __init__(self):
        pass
    
    @staticmethod
    def swap_bytes(data: bytearray) -> bytearray:
        """Apply byte swapping obfuscation"""
        if len(data) < 346:
            raise ValueError(f"Data too short for byte swapping: {len(data)} < 346")
        
        # Apply the same byte swaps as the Swift version
        data[3], data[5] = data[5], data[3]
        data[8], data[17] = data[17], data[8]
        data[128], data[345] = data[345], data[128]
        data[15], data[65] = data[65], data[15]
        data[33], data[133] = data[133], data[33]
        data[16], data[64] = data[64], data[16]
        
        return data
    
    @staticmethod
    def calculate_password() -> str:
        """Calculate the decryption password using the same logic as Swift"""
        i = 4 * 2 * 4 * 6
        i = i * 7 / 5 + 23
        i = i - 546 * 5464564 * 64635645 * 4536454 * 462
        
        password = f"qepkwotkgpeqgpeokqgokgqoe{i}fdlgkdlgfklsdöfdgsj{i}gfdads23ji4jgi3vqewö"
        password = password.replace("q", "r")
        
        return password
    
    @staticmethod
    def decrypt(data: bytes, password: str) -> bytes:
        """
        Decrypt RNCryptor v3 encrypted data
        
        Args:
            data: Encrypted data bytes
            password: Password string
            
        Returns:
            Decrypted data bytes
        """
        if len(data) < 66:  # Minimum size for RNCryptor v3 format
            raise ValueError("Data is too short to be valid RNCryptor format")
        
        # Parse the header
        version = data[0]
        options = data[1]
        
        if version != 3:
            raise ValueError(f"Unsupported RNCryptor version: {version}")
        
        # Extract encryption salt and IV
        encryption_salt = data[2:10]
        hmac_salt = data[10:18]
        iv = data[18:34]
        
        # Encrypted data is everything except header (34 bytes) and HMAC (32 bytes at end)
        ciphertext = data[34:-32]
        expected_hmac = data[-32:]
        
        # Derive keys using PBKDF2
        encryption_key = PBKDF2(
            password,
            encryption_salt,
            dkLen=RNCryptorDecryptor.AES_KEY_SIZE,
            count=RNCryptorDecryptor.PBKDF2_ITERATIONS,
            hmac_hash_module=hashlib.sha1
        )
        
        hmac_key = PBKDF2(
            password,
            hmac_salt,
            dkLen=RNCryptorDecryptor.HMAC_KEY_SIZE,
            count=RNCryptorDecryptor.PBKDF2_ITERATIONS,
            hmac_hash_module=hashlib.sha1
        )
        
        # Verify HMAC
        hmac_message = data[:-32]  # Everything except the HMAC itself
        computed_hmac = hmac.new(hmac_key, hmac_message, hashlib.sha256).digest()
        
        if not hmac.compare_digest(computed_hmac, expected_hmac):
            raise ValueError("HMAC verification failed - incorrect password or corrupted data")
        
        # Decrypt using AES-256-CBC
        cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext)
        
        # Remove PKCS7 padding
        padding_length = plaintext[-1]
        if padding_length > 16 or padding_length == 0:
            raise ValueError("Invalid padding")
        
        plaintext = plaintext[:-padding_length]
        
        return plaintext


def decrypt_template_file(input_path: str, output_path: str, password: str = None) -> bool:
    """
    Decrypt a template file with byte swapping
    
    Args:
        input_path: Path to encrypted file
        output_path: Path to write decrypted file
        password: Optional password (calculated if not provided)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if password is None:
            password = RNCryptorDecryptor.calculate_password()
        
        # Read encrypted data
        with open(input_path, 'rb') as f:
            encrypted_data = bytearray(f.read())
        
        # First byte swap (deobfuscation)
        encrypted_data = RNCryptorDecryptor.swap_bytes(encrypted_data)
        
        # Decrypt
        decrypted_data = RNCryptorDecryptor.decrypt(bytes(encrypted_data), password)
        
        # Second byte swap (deobfuscation)
        decrypted_data = bytearray(decrypted_data)
        decrypted_data = RNCryptorDecryptor.swap_bytes(decrypted_data)
        
        # Write output
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)
        
        print(f"[SUCCESS] Decrypted {input_path} -> {output_path}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to decrypt {input_path}: {e}")
        return False


if __name__ == "__main__":
    # Test the decryption
    print("RNCryptor Decryptor Module")
    print("Password:", RNCryptorDecryptor.calculate_password())
