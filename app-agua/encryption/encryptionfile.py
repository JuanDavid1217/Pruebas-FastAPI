from cryptography.fernet import Fernet

#key = Fernet.generate_key()
#print(key)
cifrado = Fernet(b'JSrAEQRx1HttsIedi6eI1PJIEcBn9F8tRLJctd_AwUE=')

def encrypt(mensaje: str):
    return cifrado.encrypt(mensaje.encode("utf-8"))

def desencrypt(mensaje: str): 
    #print(cifrado.decrypt(mensaje).decode())
    #return cifrado.decrypt(bytes(mensaje, encoding='utf-8')).decode()
    return cifrado.decrypt(mensaje).decode()