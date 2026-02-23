from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.models.estadoformulario import EstadoFormulario
from app.models.relacion import Relacion
from app.models.tipomutimedia import TipoMultimedia
from app.models.tokens import Token as TokenModel
from app.schemas.tokens import TokenCreate, TokenResponse
from app.utils.token_generador import generar_token_unico

router = APIRouter(prefix="/tokens", tags=["Token"])

@router.post("/", response_model=TokenResponse)
def crear_token(data: TokenCreate, db: Session = Depends(get_db)):

    token_generado = generar_token_unico(db)

    nuevo_token = TokenModel(
        IdInvitacion=data.IdInvitacion,
        IdEmpleado=data.IdEmpleado,
        Token=token_generado,
        Concretado=False
    )

    db.add(nuevo_token)
    db.commit()
    db.refresh(nuevo_token)

    return nuevo_token


@router.get("/prevista/{token}")
def prevista(token: str, db: Session = Depends(get_db)):
    estados = db.query(EstadoFormulario)\
        .join(TipoMultimedia)\
        .filter(EstadoFormulario.IdToken == token)\
        .all()

    response = {
        "showVideo": False,
        "showInfografia": False,
        "showTerms": False,
        "videoUrl": None,
        "infografiaUrl": None,
        "termsText": None
    }

    for e in estados:
        if e.TipoMultimedia.Descripcion == "VIDEO":
            response["ShowVideos"] = e.EstadoFormulario
        if e.TipoMultimedia.Descripcion == "INFOGRAFIA":
            response["ShowInfografia"] = e.EstadoFormulario
        if e.TipoMultimedia.Descripcion == "TERMINOS":
            response["ShowTerms"] = e.EstadoFormulario
            response["termsText"] = "Acepto normas de seguridad"

    return response


@router.get("/estado/{token}")
def estado_token(token: str, db: Session = Depends(get_db)):

    token_db = db.query(TokenModel).filter(TokenModel.Token == token).first()

    if not token_db:
        raise HTTPException(status_code=404, detail="Token no encontrado")
    
    total = db.query(func.count(Relacion.IdFormulario)) \
    .filter(Relacion.IdToken == token)\
    .scalar()

    completed = db.query(func.count(Relacion.IdFormulario))\
    .filter(
        EstadoFormulario.IdToken == token,
        EstadoFormulario.EstadoFormulario == True
    ).scalar()

    return{
        "valid": True,
        "total": total or 0,
        "completed": completed or 0
    }