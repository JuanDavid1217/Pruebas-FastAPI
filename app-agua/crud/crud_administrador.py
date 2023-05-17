from sqlalchemy.orm import Session
from fastapi import HTTPException

from schemas.fileschemas import GrupoCreate, GrupoBase, VinculacionCreate
from models import Grupo, Vinculacion_Grupo

from encryption.encryptionfile import encrypt, desencrypt

#----Funciones para grupos-------#

def get_all_groups(db: Session, user_id: int, skip: int = 0, limit: int = 5):
    return db.query(Grupo).filter_by(id_usuario=user_id).offset(skip).limit(limit).all()

def get_grupo_byID(db: Session, grupo_id: int):
    db_group = db.query(Grupo).filter_by(id_grupo=grupo_id).first()
    if db_group :
        return db_group
    else:
        raise HTTPException(status_code=404, detail="User not found")


#----Funciones para grupos(Vinculacion, almacenamientos-------#

#------VINCULACION------#

def add_vinculacion_group(db: Session, vinculacion: VinculacionCreate):
    db_vinculacion = Vinculacion_Grupo(id_grupo=vinculacion.id_grupo, usuario_vinculacion=vinculacion.usuario_vinculacion, 
    clave_vinculacion=encrypt(vinculacion.clave_vinculacion))
    db.add(db_vinculacion)
    db.commit()
    db.refresh(db_vinculacion)
    return db_vinculacion

def update_password_vinculacion(db: Session, grupo_id: int, newpassword: str):
    db_vinculacion = db.query(Vinculacion_Grupo).filter_by(id_grupo=grupo_id).first()

    if db_vinculacion:
        db_vinculacion.clave_vinculacion = encrypt(newpassword)
        db.commit()
        db.refresh(db_vinculacion)
    else:
        raise HTTPException(status_code=404, detail="User not found")
    return db_vinculacion

def delete_vinculacion_group(db: Session, grupo_id: int):
    db_vinculacion = db.query(Vinculacion_Grupo).filter_by(id_grupo=grupo_id).first()
    if db_vinculacion :
        db.delete(db_vinculacion)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="User not found")

def get_vinculacion(db: Session, grupo_id: int):
    db_vinculacion = db.query(Vinculacion_Grupo).filter_by(id_grupo=grupo_id).first()
    if db_vinculacion :
        return db_vinculacion
    else:
        raise HTTPException(status_code=404, detail="User not found")
    