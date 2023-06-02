from sqlalchemy.orm import Session
from fastapi import HTTPException

from encryption.encryptionfile import desencrypt

from models import Grupo, Vinculacion_Grupo

#-----el usuario Empleado(El cual se vinculara a 1 grupo) necesitara las credenciales de acceso de dicho grupo----#
def vinculacion_Empleado_Grupo(db: Session, user_name: str, password: str):
    #db_vinculacion = db.query(Vinculacion_Grupo).filter(Vinculacion_Grupo.usuario_vinculacion==user_name and desencrypt(bytes(Vinculacion_Grupo.clave_vinculacion))==password).first()
    #if db_vinculacion:
    #    db_grupo = db.query(Grupo).filter_by(id_grupo=db_vinculacion.id_grupo).first()
    #    return db_grupo
    #else:
    #    raise HTTPException(status_code=404, detail="User or Password are incorrect")

    
    db_vinculacion = db.query(Vinculacion_Grupo).filter_by(usuario_vinculacion=user_name).first()
    if db_vinculacion!=None and desencrypt(db_vinculacion.clave_vinculacion)==password:
        db_grupo = db.query(Grupo).filter_by(id_grupo=db_vinculacion.id_grupo).first()
        return db_grupo
    else:
        raise HTTPException(status_code=404, detail="User or password are incorrect")