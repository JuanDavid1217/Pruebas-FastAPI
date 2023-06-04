from sqlalchemy.orm import Session

from schemas.fileschemas import UserCreate
from models import Usuario

from fastapi import HTTPException#, Response
#from starlette.status import HTTP_400_BAD_REQUEST

from encryption.encryptionfile import encrypt, desencrypt, validarpassword

#-----Funcion principal---------#
def create_user(db: Session, user: UserCreate):
    #encrypther_password = cifrado.encrypt(user.password.encode("utf-8")) #Implementa la funcion para encriptarlo
    usuario=db.query(Usuario).filter_by(usuario=user.usuario).first()
    if usuario==None:
        bandera=validarpassword(user.password)
        if bandera==1:
            db_user = Usuario(usuario=user.usuario, password=encrypt(user.password), id_tipo=user.id_tipo)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        else:
            raise HTTPException(status_code=300, detail="invalid password")
    else:
        raise HTTPException(status_code=300, detail="user already exist")
        #return None
    


def update_user(db: Session, user_id: int, newuser: UserCreate):
    db_usuario = db.query(Usuario).filter_by(id_usuario=user_id).first()
    usuario1 = db.query(Usuario).filter_by(usuario=newuser.usuario).first()
    if db_usuario:
        if db_usuario==usuario1 or usuario1==None:
            bandera=validarpassword(newuser.password)
            if bandera==1:
                db_usuario.usuario = newuser.usuario
                db_usuario.password = encrypt(newuser.password)
                db_usuario.id_tipo = newuser.id_tipo
                db.commit()
                db.refresh(db_usuario)
                return db_usuario
            raise HTTPException(status_code=300, detail="invalid password")
        else:
            raise HTTPException(status_code=300, detail="user already exist")
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
    
   
def delete_user(db: Session, user_id:int):
    db_usuario = db.query(Usuario).filter_by(id_usuario=user_id).first()

    if db_usuario :
        db.delete(db_usuario)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="User not found")


def get_user_by_UP(db: Session, user_name: str, password: str):
    #db_usuario = db.query(Usuario).filter(Usuario.usuario==user_name and (desencrypt(bytes(Usuario.password))==password)).first()
    db_usuario = db.query(Usuario).filter_by(usuario=user_name).first()
    if db_usuario!=None and desencrypt(db_usuario.password)==password:
        return db_usuario
    else:
        raise HTTPException(status_code=404, detail="User or password are incorrect")