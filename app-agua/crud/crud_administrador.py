from sqlalchemy.orm import Session
from fastapi import HTTPException

from schemas.fileschemas import GrupoCreate, GrupoBase, VinculacionCreate
from models import Grupo, Vinculacion_Grupo, Usuario

from encryption.encryptionfile import encrypt, desencrypt, validarpassword

#----Funciones para grupos-------#

def get_all_groups(db: Session, user_id: int, skip: int = 0, limit: int = 5):
    return db.query(Grupo).filter_by(id_usuario=user_id).offset(skip).limit(limit).all()

def get_grupo_byID(db: Session, grupo_id: int):
    db_group = db.query(Grupo).filter_by(id_grupo=grupo_id).first()
    if db_group :
        return db_group
    else:
        raise HTTPException(status_code=404, detail="Group not found")


#----Funciones para grupos(Vinculacion, almacenamientos-------#

#------VINCULACION------#

def add_vinculacion_group(db: Session, vinculacion: VinculacionCreate):
    grupo=db.query(Grupo).filter_by(id_grupo=vinculacion.id_grupo).first()
    if grupo:
        user=db.query(Usuario).filter_by(id_usuario=grupo.id_usuario).first()
        if user.id_tipo==1:
            vinculacion1=db.query(Vinculacion_Grupo).filter_by(id_grupo=vinculacion.id_grupo).first()
            vinculacion2=db.query(Vinculacion_Grupo).filter_by(usuario_vinculacion=vinculacion.usuario_vinculacion).first()
            if vinculacion1==None:
                if vinculacion2==None:
                    bandera=validarpassword(vinculacion.clave_vinculacion)
                    if bandera==1:
                        db_vinculacion = Vinculacion_Grupo(id_grupo=vinculacion.id_grupo, usuario_vinculacion=vinculacion.usuario_vinculacion, 
                        clave_vinculacion=encrypt(vinculacion.clave_vinculacion))
                        db.add(db_vinculacion)
                        db.commit()
                        db.refresh(db_vinculacion)
                        return db_vinculacion
                    else:
                        raise HTTPException(status_code=300, detail="invalid clave")
                else:
                    raise HTTPException(status_code=300, detail="user already exist")
            else:
                raise HTTPException(status_code=300, detail="group already have a vinculation")
        else:
            raise HTTPException(status_code=300, detail="Don't are an administrator")
    else:
        raise HTTPException(status_code=404, detail="Group not found")
    

def update_password_vinculacion(db: Session, grupo_id: int, newpassword: str):
    db_vinculacion = db.query(Vinculacion_Grupo).filter_by(id_grupo=grupo_id).first()

    if db_vinculacion:
        bandera=validarpassword(newpassword)
        if bandera==1:
            db_vinculacion.clave_vinculacion = encrypt(newpassword)
            db.commit()
            db.refresh(db_vinculacion)
            return db_vinculacion
        else:
            raise HTTPException(status_code=300, detail="invalid clave")
    else:
        raise HTTPException(status_code=404, detail="Group not found")

def delete_vinculacion_group(db: Session, grupo_id: int):
    db_vinculacion = db.query(Vinculacion_Grupo).filter_by(id_grupo=grupo_id).first()
    if db_vinculacion :
        db.delete(db_vinculacion)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="vinculation not found")

def get_vinculacion(db: Session, grupo_id: int):
    db_vinculacion = db.query(Vinculacion_Grupo).filter_by(id_grupo=grupo_id).first()
    if db_vinculacion :
        return db_vinculacion
    else:
        raise HTTPException(status_code=404, detail="vinculation not found")
    