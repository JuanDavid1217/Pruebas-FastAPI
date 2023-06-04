from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from .session_file import get_db
from schemas.fileschemas import Recepcion_Datos, Recepcion_DatosVin, Entrada_Agua, Entrada_AguaVin, Salida_Agua, Salida_AguaVin
from crud import crud_IoT as crud


router = APIRouter(
    prefix="/IoT",
    tags=["IoT"],
    responses={404: {"description": "Not found"}},
)

@router.post("/variables/", response_model=Recepcion_Datos)
def save_variables(dispoIoT: Recepcion_DatosVin, db: Session = Depends(get_db)):
    return crud.save_variables(db=db, dispoIoT=dispoIoT)

@router.post("/entrada/", response_model=Entrada_Agua)
def save_entrada(entradaAgua: Entrada_AguaVin, db: Session = Depends(get_db)):
    return crud.save_entradaAgua(db=db, entradaAgua=entradaAgua)

@router.post("/salida/", response_model=Salida_Agua)
def save_salida(salidaAgua: Salida_AguaVin, db: Session = Depends(get_db)):
    return crud.save_salidaAgua(db=db, salidaAgua=salidaAgua)

@router.get("/analisis/{almacenamiento_id}/{fecha_inicio}/{fecha_fin}")
def analisis(fecha_inicio: str, fecha_fin: str, almacenamiento_id: int, db: Session = Depends(get_db)):
    return crud.get_Entradabydate(db=db, fech_inicio=fecha_inicio, fech_fin=fecha_fin, almacenamiento_id=almacenamiento_id)