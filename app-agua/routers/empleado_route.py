from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from .session_file import get_db
from schemas.fileschemas import Grupo
from crud import crud_empleado as crud

router = APIRouter(
    prefix="/Empleado",
    tags=["empleado"],
    responses={404: {"description": "Not found"}},
)



@router.get("/{user_name}/{password}", response_model=Grupo)
def access_vinculacion(user_name: str, password: str, db: Session = Depends(get_db)):
    return crud.vinculacion_Empleado_Grupo(db=db, user_name=user_name, password=password)