from sqlalchemy.orm import Session

from schemas.fileschemas import UserCreate
from models import Usuario

from fastapi import HTTPException#, Response
#from starlette.status import HTTP_400_BAD_REQUEST

from encryption.encryptionfile import encrypt, desencrypt

#-----Funcion principal---------#
def create_user(db: Session, user: UserCreate):
    #encrypther_password = cifrado.encrypt(user.password.encode("utf-8")) #Implementa la funcion para encriptarlo
    
        db_user = Usuario(usuario=user.usuario, password=encrypt(user.password), id_tipo=user.id_tipo)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    


def update_user(db: Session, user_id: int, newuser: UserCreate):
    db_usuario = db.query(Usuario).filter_by(id_usuario=user_id).first()

    if db_usuario:
        db_usuario.usuario = newuser.usuario
        db_usuario.password = encrypt(newuser.password)
        db_usuario.id_tipo = newuser.id_tipo
        db.commit()
        db.refresh(db_usuario)
    else:
        raise HTTPException(status_code=404, detail="User not found")
    return db_usuario

    
    
   
def delete_user(db: Session, user_id:int):
    db_usuario = db.query(Usuario).filter_by(id_usuario=user_id).first()

    if db_usuario :
        db.delete(db_usuario)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="User not found")


def get_user_by_UP(db: Session, user_name: str, password: str):
    db_usuario = db.query(Usuario).filter(Usuario.usuario==user_name and desencrypt(bytes(Usuario.password))==password).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="User or password are incorrect")
    return db_usuario