from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from .session_file import get_db
from schemas.fileschemas import GrupoCreate, Grupo, GrupoBase, Almacenamiento, AlmacenamientoCreate, IoT, IoTCreate, Usuario
from crud import crud_generalUsers as crud

router = APIRouter(
    prefix="/Administrador-Casa",
    tags=["administrador-Casa"],
    responses={404: {"description": "Not found"}},
)

#-----Acciones a realizar sobre grupos------#
@router.post("/Grupo/", response_model=Grupo)
def create_grupo(grupo: GrupoCreate, db: Session = Depends(get_db)):
    return crud.create_group(db=db, grupo=grupo)

@router.put("/Grupo/{grupo_id}", response_model=Grupo)
def update_grupo(grupo_id: int, grupo: GrupoBase, db: Session = Depends(get_db)):
    return crud.update_group(db=db, grupo_id=grupo_id, grupo=grupo)

@router.delete("/Grupo/{grupo_id}")
def delete_grupo(grupo_id: int, db: Session = Depends(get_db)):
    return crud.delete_group(db=db, grupo_id=grupo_id)

@router.get("/Grupo/{grupo_id}")
def getNamesUserGruop(grupo_id: int, db: Session = Depends(get_db)):
    return crud.getNamesUserGruop(db=db, grupo_id=grupo_id)

    
#------Acciones sobre almacenamientos------#

@router.post("/Almacenamiento/", response_model=Almacenamiento)
def add_almacenamiento(almacenamiento: AlmacenamientoCreate, db: Session = Depends(get_db)):
    return crud.add_almacenamiento(db=db, almacenamiento=almacenamiento)

@router.put("/Almacenamiento/{almacenamiento_id}", response_model=Almacenamiento)
def update_almacenamiento(almacenamiento_id: int, almacenamiento: AlmacenamientoCreate, db: Session = Depends(get_db)):
    return crud.update_almacenamiento(db=db, almacenamiento_id=almacenamiento_id, almacenamiento=almacenamiento)

@router.delete("/Almacenamiento/{almacenamiento_id}")
def delete_almacenamiento(almacenamiento_id: int, db: Session = Depends(get_db)):
    return crud.delete_almacenamiento(db=db, almacenamiento_id=almacenamiento_id)

@router.get("/Almacenamientos/{grupo_id}", response_model=list[Almacenamiento])
def get_almacenamientosbyGroup(grupo_id: int, db: Session = Depends(get_db)):
    return crud.get_almacenamientos(db=db, grupo_id=grupo_id)

@router.get("/Almacenamiento/{almacenamiento_id}", response_model=Almacenamiento)
def get_almacenamiento_byID(almacenamiento_id: int, db: Session = Depends(get_db)):
    return crud.get_almacenamiento_byID(db=db, almacenamiento_id=almacenamiento_id)

@router.post("/Almacenamiento/IoT/", response_model=IoT)
def add_dispoIoT(dispo: IoTCreate, db: Session =  Depends(get_db)):
    return crud.vincular_IoT(db=db, dispo=dispo)

@router.get("/Almacenamiento/IoT/{almacenamiento_id}", response_model=IoT)
def get_IoTName(almacenamiento_id: int, db: Session = Depends(get_db)):
    return crud.get_IoTName(db=db, id_almacenamiento=almacenamiento_id)

@router.get("/{id_almacenamiento}")
def getIdUserbyIDAlma(id_almacenamiento: int, db: Session = Depends(get_db)):
    return crud.get_User_by_IDAlma(db=db, id_alma=id_almacenamiento)