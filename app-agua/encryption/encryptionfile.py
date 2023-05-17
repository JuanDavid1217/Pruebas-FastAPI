from cryptography.fernet import Fernet

key = Fernet.generate_key()
cifrado = Fernet(key)

def encrypt(mensaje: str):
    return cifrado.encrypt(mensaje.encode("utf-8"))

def desencrypt(mensaje: str): 
    return cifrado.decrypt(bytes(mensaje)).decode()