from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from .session_file import get_db
from schemas import fileschemas as schemas
from crud import crud_principal as crud

router = APIRouter(
    prefix="/General-Users",
    tags=["usuarios-general"],
    responses={404: {"description": "Not found"}},
)



@router.post("/", response_model=schemas.Usuario)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@router.put("/{user_id}", response_model=schemas.Usuario)
def update_user(user_id: int, newuser: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.update_user(db=db, user_id=user_id, newuser=newuser)

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db=db, user_id=user_id)

@router.get("/{user_name}/{password}", response_model=schemas.Usuario)
def access_acount(user_name: str, password: str, db: Session = Depends(get_db)):
    return crud.get_user_by_UP(db=db, user_name=user_name, password=password)