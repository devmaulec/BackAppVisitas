from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.tokens import Token
from app.models.invitacion import Invitacion
from app.schemas.invitacion import InvitacionCreate, InvitacionResponse
from app.utils.token_generador import generar_token

router = APIRouter(prefix="/invitacion", tags=["Invitacion"])

@router.post("/", response_model=InvitacionResponse)
def crear_invitacion(dto: InvitacionCreate, db: Session = Depends(get_db)):

    nueva_invitacion = Invitacion(**dto.dict())

    db.add(nueva_invitacion)
    db.commit()
    db.refresh(nueva_invitacion)


    token_generado = generar_token()

    nuevo_token = Token(
        IdInvitacion=nueva_invitacion.IdInvitacion,
        Token=token_generado
    )

    db.add(nuevo_token)
    db.commit()

    return nueva_invitacion