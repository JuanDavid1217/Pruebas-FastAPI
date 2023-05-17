from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import Grupo

#-----La sig funcion sera solo para el usario Casa-----#
def get_grupo_byUser(db: Session, user_id: int):
    db_group = db.query(Grupo).filter_by(id_usuario=user_id).first()
    if not db_group :
        db_group=[]
    return db_group
    
        