from cryptography.fernet import Fernet
import re

#key = Fernet.generate_key()
#print(key)
cifrado = Fernet(b'JSrAEQRx1HttsIedi6eI1PJIEcBn9F8tRLJctd_AwUE=')

def encrypt(mensaje: str):
    return cifrado.encrypt(mensaje.encode("utf-8"))

def desencrypt(mensaje: str): 
    #print(cifrado.decrypt(mensaje).decode())
    #return cifrado.decrypt(bytes(mensaje, encoding='utf-8')).decode()
    return cifrado.decrypt(mensaje).decode()

def validarpassword(password: str):
    prueba=re.compile('^(?=.*\d)(?=.*[\u0021-\u002b\u003c-\u0040])(?=.*[A-Z])(?=.*[a-z])\S{8,16}$')
    pase=prueba.match(password)
    if pase:
        return 1
    else:
        return 2
