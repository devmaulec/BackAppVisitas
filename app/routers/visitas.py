from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.tokens import Token
from app.models.visitas import Visita
from app.schemas.visita import VisitaCreate, VisitaResponse
from app.utils.token_generador import generar_token

router = APIRouter(prefix="/visitas", tags=["Visitas"])

@router.post("/", response_model=VisitaResponse)
def crear_visita(dto: VisitaCreate, db: Session = Depends(get_db)):

    nueva_visita = Visita(**dto.dict())

    db.add(nueva_visita)
    db.commit()
    db.refresh(nueva_visita)

    # 🔥 generar token
    token_generado = generar_token()

    nuevo_token = Token(
        IdVisita=nueva_visita.IdVisita,
        Token=token_generado
    )

    db.add(nuevo_token)
    db.commit()

    return nueva_visita

    return visita


@router.get("/", response_model=list[VisitaResponse])
def listar_visitas(db: Session = Depends(get_db)):
    return db.query(Visita).all()