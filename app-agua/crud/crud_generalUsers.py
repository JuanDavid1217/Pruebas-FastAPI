from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException

from schemas.fileschemas import GrupoCreate, GrupoBase, AlmacenamientoCreate, IoTCreate
from models import Grupo, Vinculacion_Grupo, Almacenamiento, IoT, Usuario
from crud.crud_administrador import get_all_groups

#-----Esatas funciones las ocuparia el Admin y Casa-----#

#---esta funcion, el usuario Casa solo la podra usar 1 vez-----#
def create_group(db: Session, grupo: GrupoCreate):
    grupos=get_all_groups(db, grupo.id_usuario)
    user=db.query(Usuario).filter_by(id_usuario=grupo.id_usuario).first()
    valor=0

    if user.id_tipo==1:
        valor=5
    else:
        valor=1
    
    if(len(grupos)<valor):
        #grupo1=db.query(Grupo).filter_by(nombre=grupo.nombre).first()#Esto es molesto
        bandera=0
        for g in grupos:
            if g.nombre==grupo.nombre:
                bandera=1

        if bandera==0:
            db_group = Grupo(id_usuario=grupo.id_usuario, nombre=grupo.nombre)
            db.add(db_group)
            db.commit()
            db.refresh(db_group)
            return db_group
        else:
            raise HTTPException(status_code=300, detail="Group name already exist")
    else:
        raise HTTPException(status_code=300, detail=f"You already have {len(grupos)} registered groups")

def update_group(db: Session, grupo_id: int, grupo:GrupoBase):
    db_group = db.query(Grupo).filter_by(id_grupo=grupo_id).first()
    #grupo1 = db.query(Grupo).filter_by(nombre=grupo.nombre).first()#Esto es molesto
    if db_group:
        bandera=0
        grupos=get_all_groups(db, db_group.id_usuario)
        for g in grupos:
            if g.nombre==grupo.nombre:
                bandera=1

        if bandera==0:
            db_group.nombre = grupo.nombre
            db.commit()
            db.refresh(db_group)
            return db_group
        else:
            raise HTTPException(status_code=300, detail="Group name already exist")
    else:
        raise HTTPException(status_code=404, detail="Group not found")
    

def delete_group(db: Session, grupo_id: int):
    db_group = db.query(Grupo).filter_by(id_grupo=grupo_id).first()
    if db_group :
        db.delete(db_group)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Group not found")

def getNamesUserGruop(db:Session, grupo_id: int):
    grupo=db.query(Grupo.nombre, Grupo.id_usuario).filter_by(id_grupo=grupo_id).first()
    if(grupo):
        user=db.query(Usuario.usuario).filter_by(id_usuario=grupo[1]).first()
        return {"usuario":user[0],
                "grupo":grupo[0]}
    else:
        raise HTTPException(status_code=404, detail="Group not found")

#-----Almacenamientos------#
def add_almacenamiento(db: Session, almacenamiento: AlmacenamientoCreate):
    almacenamientos=get_almacenamientos(db, almacenamiento.id_grupo)
    if(len(almacenamientos)<5):
        bandera=0
        for a in almacenamientos:
            if a.ubicacion==almacenamiento.ubicacion:
                bandera=1

        if bandera==0:
            if(almacenamiento.capacidad_maxima>=250 and almacenamiento.capacidad_maxima<=25000):
                db_almacenamiento = Almacenamiento(id_grupo=almacenamiento.id_grupo, capacidad_maxima=almacenamiento.capacidad_maxima,
                ubicacion=almacenamiento.ubicacion)
                db.add(db_almacenamiento)
                db.commit()
                db.refresh(db_almacenamiento)
                return db_almacenamiento
            else:
                raise HTTPException(status_code=300, detail="Tank's capacity is out of valid range")
        else:
            raise HTTPException(status_code=300, detail="Tank's ubication already exist")
    else:
        raise HTTPException(status_code=300, detail="You already have 5 registered water tanks")

def update_almacenamiento(db: Session, almacenamiento_id: int, almacenamiento: AlmacenamientoCreate):
    #Preguntar si combiene pasar todo el objeto o solo el parametro a modificar
    db_almacenamiento = db.query(Almacenamiento).filter_by(id_almacenamiento=almacenamiento_id).first()

    if db_almacenamiento:
        bandera=0
        almacenamientos=get_almacenamientos(db, almacenamiento.id_grupo)
        for a in almacenamientos:
            if (a.ubicacion==almacenamiento.ubicacion) and (a.id_almacenamiento!=db_almacenamiento.id_almacenamiento):
                bandera=1
        if bandera==0:
            if (almacenamiento.capacidad_maxima>=250 and almacenamiento.capacidad_maxima<=25000):
                db_almacenamiento.capacidad_maxima = almacenamiento.capacidad_maxima
                db_almacenamiento.ubicacion = almacenamiento.ubicacion
                db.commit()
                db.refresh(db_almacenamiento)
                return db_almacenamiento
            else:
                raise HTTPException(status_code=300, detail="Tank's capacity is out of valid range")
        else:
            raise HTTPException(status_code=300, detail="Tank's ubication already exist")
    else:
        raise HTTPException(status_code=404, detail="Almacenamiento not found")

def delete_almacenamiento(db:Session, almacenamiento_id: int):
    db_almacenamiento = db.query(Almacenamiento).filter_by(id_almacenamiento=almacenamiento_id).first()

    if db_almacenamiento :
        db.delete(db_almacenamiento)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Almacenamiento not found")

def get_almacenamientos(db:Session, grupo_id: int, skip: int = 0, limit: int = 5):
    db_almacenamientos = db.query(Almacenamiento).filter_by(id_grupo=grupo_id).offset(skip).limit(limit).all()
    #if db_almacenamientos:
    #    return db_almacenamientos
    #else:
    #    raise HTTPException(status_code=404, detail="Almacenamientos not founds")
    return db_almacenamientos

def get_almacenamiento_byID(db:Session, almacenamiento_id: int):
    db_almacenamiento = db.query(Almacenamiento).filter_by(id_almacenamiento=almacenamiento_id).first()
    if db_almacenamiento:
        return db_almacenamiento
    else:
        raise HTTPException(status_code=404, detail="Almacenamiento not found")


def vincular_IoT(db:Session, dispo:IoTCreate):
    try:
        almacenamiento=get_almacenamiento_byID(db, dispo.id_almacenamiento)
        if almacenamiento:
            dispo1=db.query(IoT).filter_by(dispo_IoT=dispo.dispo_IoT).first()
            if dispo1==None:
                db_dispo = IoT(id_almacenamiento=dispo.id_almacenamiento, dispo_IoT=dispo.dispo_IoT)
                db.add(db_dispo)
                db.commit()
                db.refresh(db_dispo)
                return db_dispo
            else:
                raise HTTPException(status_code=303, detail="IoT name already exist")
        else:
            raise HTTPException(status_code=404, detail="Almacenamiento not found")
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")        

def get_IoTName(db:Session, id_almacenamiento: int):
    db_IoT=db.query(IoT).filter_by(id_almacenamiento=id_almacenamiento).first()
    if(db_IoT):
        return db_IoT
    else:
        raise HTTPException(status_code=404, detail="IoT not found")

def get_User_by_IDAlma(db:Session, id_alma:int):
    id_grupo=db.query(Almacenamiento.id_grupo).filter_by(id_almacenamiento=id_alma).first()
    if(id_grupo):
        id_user=db.query(Grupo.id_usuario).filter_by(id_grupo=id_grupo[0]).first()
        return {'id_usuario': id_user[0]}
    else:
        raise HTTPException(status_code=404, detail="Almacenamiento not found")
    
        

