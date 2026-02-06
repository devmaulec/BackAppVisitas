from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.personal_visita import PersonalVisita
from app.schemas.personal_visita import PersonalVisitaCreate, PersonalVisitaResponse

router = APIRouter(prefix="/personal-visita", tags=["Personal Visita"])

@router.post("/", response_model=PersonalVisitaResponse)
def registrar_personal(data: PersonalVisitaCreate, db: Session = Depends(get_db)):
    nuevo = PersonalVisita(**data.dict())

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo