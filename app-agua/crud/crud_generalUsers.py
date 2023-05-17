from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException

from schemas.fileschemas import GrupoCreate, GrupoBase, AlmacenamientoCreate, IoTCreate
from models import Grupo, Vinculacion_Grupo, Almacenamiento, IoT

#-----Esatas funciones las ocuparia el Admin y Casa-----#

#---esta funcion, el usuario Casa solo la podra usar 1 vez-----#
def create_group(db: Session, grupo: GrupoCreate):
    db_group = Grupo(id_usuario=grupo.id_usuario, nombre=grupo.nombre)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def update_group(db: Session, grupo_id: int, grupo:GrupoBase):
    db_group = db.query(Grupo).filter_by(id_grupo=grupo_id).first()

    if db_group:
        db_group.nombre = grupo.nombre
        db.commit()
        db.refresh(db_group)
    else:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group

def delete_group(db: Session, grupo_id: int):
    db_group = db.query(Grupo).filter_by(id_grupo=grupo_id).first()

    if db_group :
        db.delete(db_group)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Group not found")

#-----Almacenamientos------#
def add_almacenamiento(db: Session, almacenamiento: AlmacenamientoCreate):
    db_almacenamiento = Almacenamiento(id_grupo=almacenamiento.id_grupo, capacidad_maxima=almacenamiento.capacidad_maxima,
    ubicacion=almacenamiento.ubicacion)
    db.add(db_almacenamiento)
    db.commit()
    db.refresh(db_almacenamiento)
    return db_almacenamiento

def update_almacenamiento(db: Session, almacenamiento_id: int, almacenamiento: AlmacenamientoCreate):
    #Preguntar si combiene pasar todo el objeto o solo el parametro a modificar
    db_almacenamiento = db.query(Almacenamiento).filter_by(id_almacenamiento=almacenamiento_id).first()

    if db_almacenamiento:
        db_almacenamiento.capacidad_maxima = almacenamiento.capacidad_maxima
        db_almacenamiento.ubicacion = almacenamiento.ubicacion
        db.commit()
        db.refresh(db_almacenamiento)
    else:
        raise HTTPException(status_code=404, detail="Almacenamiento not found")
    return db_almacenamiento

def delete_almacenamiento(db:Session, almacenamiento_id: int):
    db_almacenamiento = db.query(Almacenamiento).filter_by(id_almacenamiento=almacenamiento_id).first()

    if db_almacenamiento :
        db.delete(db_almacenamiento)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Almacenamiento not found")

def get_almacenamientos(db:Session, grupo_id: int):
    db_almacenamientos = db.query(Almacenamiento).filter_by(id_grupo=grupo_id).all()
    if db_almacenamientos:
        return db_almacenamientos
    else:
        raise HTTPException(status_code=404, detail="Almacenamientos not founds")
    

def get_almacenamiento_byID(db:Session, almacenamiento_id: int):
    db_almacenamiento = db.query(Almacenamiento).filter_by(id_almacenamiento=almacenamiento_id).first()
    if db_almacenamiento:
        return db_almacenamiento
    else:
        raise HTTPException(status_code=404, detail="Almacenamiento not found")


def vincular_IoT(db:Session, dispo:IoTCreate):
    db_dispo = IoT(id_almacenamiento=dispo.id_almacenamiento, dispo_IoT=dispo.dispo_IoT)
    db.add(db_dispo)
    db.commit()
    db.refresh(db_dispo)
    return db_dispo


def get_Entradabydate(db:Session, almacenmiento_id: int, fech_inicio: str, fech_fin: str):
    id_vinculacion=db.query(IoT.id_vin_IoT).filter_by(id_almacenamiento=almacenamiento_id).first()
    if id_vinculacion:
        db_entrada = db.query(Entrada_Agua).filter(Entrada_Agua.id_almacenamiento==almacenamiento_id and
        Entrada_Agua.Fecha_Hora)        

