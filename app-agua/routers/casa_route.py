from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from .session_file import get_db
from schemas.fileschemas import Grupo
from crud import crud_casa as crud

router = APIRouter(
    prefix="/Casa",
    tags=["casa"],
    responses={404: {"description": "Not found"}},
)



@router.get("/{user_id}", response_model=Grupo)
def get_group(user_id: int, db: Session = Depends(get_db)):
    return crud.get_grupo_byUser(db=db, user_id=user_id)