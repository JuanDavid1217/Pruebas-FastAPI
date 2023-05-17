from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from .session_file import get_db
from schemas.fileschemas import VinculacionCreate, Vinculacion_Grupo, Grupo
from crud import crud_administrador as crud

router = APIRouter(
    prefix="/Administrador",
    tags=["administrador"],
    responses={404: {"description": "Not found"}},
)



@router.post("/", response_model=Vinculacion_Grupo)
def add_vinculacion(vinculacion: VinculacionCreate, db: Session = Depends(get_db)):
    return crud.add_vinculacion_group(db=db, vinculacion=vinculacion)

@router.put("/{grupo_id}/{newpassword}", response_model=Vinculacion_Grupo)
def update_password(grupo_id: int, newpassword: str, db: Session = Depends(get_db)):
    return crud.update_password_vinculacion(db=db, grupo_id=grupo_id, newpassword=newpassword)

@router.delete("/{grupo_id}")
def delete_vinculacion(grupo_id: int, db: Session = Depends(get_db)):
    return crud.delete_vinculacion_group(db=db, grupo_id=grupo_id)

@router.get("/Vinculacion/{grupo_id}", response_model=Vinculacion_Grupo)
def get_user_vinculation(grupo_id: int, db: Session = Depends(get_db)):
    return crud.get_vinculacion(db=db, grupo_id=grupo_id)

@router.get("/Grupos/{user_id}", response_model=list[Grupo])
def get_all_groups(user_id: int, db: Session = Depends(get_db)):
    return crud.get_all_groups(db=db, user_id=user_id)

@router.get("/Grupo/{group_id}", response_model=Grupo)
def get_groupbyID(group_id: int, db: Session = Depends(get_db)):
    return crud.get_grupo_byID(db=db, grupo_id=group_id)
