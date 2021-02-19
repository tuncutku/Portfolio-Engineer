from cryptography.fernet import Fernet
import os


def generate_key():
    """
    Generates a key and save it into a file
    """
    return Fernet.generate_key()


def encrypt_token(token: str) -> str:
    """
    Encrypts a message
    """
    key = bytes(os.environ["ENCRYPTION_KEY"].encode("utf-8"))
    encoded_token = token.encode()
    f = Fernet(key)
    return f.encrypt(encoded_token).decode()


def decrypt_token(encrypted_token: str) -> str:
    """
    Decrypts an encrypted message
    """
    key = bytes(os.environ["ENCRYPTION_KEY"].encode("utf-8"))
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_token.encode("utf-8"))

    return decrypted_message.decode()
