from cryptography.fernet import Fernet
import os

def generate_key():
    """
    Generates a key and save it into a file
    """
    return Fernet.generate_key()

def encrypt_token(token):
    """
    Encrypts a message
    """
    #key = os.environ["ENCRYPTION_KEY"]
    key = bytes(b'ViRCBRodlTc1fYrOWF0YCRzgDcE_2ovGJDgsQT0gvuA=')
    encoded_token = token.encode()
    f = Fernet(key)
    return f.encrypt(encoded_token)

def decrypt_token(encrypted_token):
    """
    Decrypts an encrypted message
    """
    # key = os.environ["ENCRYPTION_KEY"]
    key = bytes(b'ViRCBRodlTc1fYrOWF0YCRzgDcE_2ovGJDgsQT0gvuA=')
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_token)

    return decrypted_message.decode()

token = encrypt_token("hello world")
message = decrypt_token(token)

a =1
