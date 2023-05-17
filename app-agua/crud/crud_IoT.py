from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException

from schemas.fileschemas import Recepcion_DatosVin, Entrada_AguaVin, Salida_AguaVin
from models import IoT, Recepcion_Datos, Entrada_Agua, Salida_Agua

from fastapi.encoders import jsonable_encoder


def get_IdVinculacion(db: Session, dispo: str):
    id_vinculacion=db.query(IoT.id_vin_IoT).filter_by(dispo_IoT=dispo).first()
    if id_vinculacion:
        id_vinculacion=id_vinculacion[0]
    return id_vinculacion
    print(id_vinculacion)


def save_variables(db: Session, dispoIoT: Recepcion_DatosVin):
    id_vinculacion=get_IdVinculacion(db=db, dispo=dispoIoT.dispo_IoT)
    if id_vinculacion:
        db_variables = Recepcion_Datos(id_vin_IoT=id_vinculacion, nivel_actual=dispoIoT.nivel_actual,
        Boya1=dispoIoT.Boya1, Boya2=dispoIoT.Boya2, Boya3=dispoIoT.Boya3, BoyaP=dispoIoT.BoyaP,
        Estado_Bomba=dispoIoT.Estado_Bomba, Fecha_Hora=dispoIoT.Fecha_Hora)
        db.add(db_variables)
        db.commit()
        db.refresh(db_variables)
        return jsonable_encoder(db_variables)
    else:
        raise HTTPException(status_code=404, detail="Dispositivo IoT NO VINCULADO")

def save_entradaAgua(db: Session, entradaAgua: Entrada_AguaVin):
    id_vinculacion=get_IdVinculacion(db, entradaAgua.dispo_IoT)
    if id_vinculacion :
        db_entrada = Entrada_Agua(id_vin_IoT=id_vinculacion, cantidad_entrada=entradaAgua.cantidad_entrada,
        Fecha_Hora=entradaAgua.Fecha_Hora)
        db.add(db_entrada)
        db.commit()
        db.refresh(db_entrada)
        return jsonable_encoder(db_entrada)
    else:
        raise HTTPException(status_code=404, detail="Dispositivo IoT NO VINCULADO")

def save_salidaAgua(db: Session, salidaAgua: Salida_AguaVin):
    id_vinculacion=get_IdVinculacion(db, salidaAgua.dispo_IoT)
    if id_vinculacion :
        db_salida = Salida_Agua(id_vin_IoT=id_vinculacion, cantidad_salida=salidaAgua.cantidad_salida,
        Fecha_Hora=salidaAgua.Fecha_Hora)
        db.add(db_salida)
        db.commit()
        db.refresh(db_salida)
        return jsonable_encoder(db_salida)
    else:
        raise HTTPException(status_code=404, detail="Dispositivo IoT NO VINCULADO")