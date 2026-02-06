from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.models.tokens import Token as TokenModel
from app.schemas.tokens import TokenCreate, TokenResponse
from app.utils.token_generador import generar_token_unico

router = APIRouter(prefix="/tokens", tags=["Tokens"])


@router.post("/", response_model=TokenResponse)
def crear_token(data: TokenCreate, db: Session = Depends(get_db)):

    token_generado = generar_token_unico(db)

    nuevo_token = TokenModel(
        IdVisita=data.IdVisita,
        IdEmpleado=data.IdEmpleado,
        Token=token_generado,
        ShowVideo=True,
        ShowInfografia=True,
        ShowTerms=True,
        FechaHoraEntrada=None,
        FechaHoraSalida=None,
        Concretado=True
    )

    db.add(nuevo_token)
    db.commit()
    db.refresh(nuevo_token)

    return nuevo_token


@router.get("/{id_token}", response_model=TokenResponse)
def obtener_token(id_token: int, db: Session = Depends(get_db)):

    token = db.query(TokenModel)\
              .filter(TokenModel.IdToken == id_token)\
              .first()

    if not token:
        raise HTTPException(status_code=404, detail="Token no encontrado")

    return token


@router.get("/validar/{codigo}", response_model=TokenResponse)
def validar_token(codigo: str, db: Session = Depends(get_db)):

    token = db.query(TokenModel)\
              .filter(TokenModel.Token == codigo)\
              .first()

    if not token:
        raise HTTPException(status_code=404, detail="Token inválido")

    if token.Concretado:
        raise HTTPException(status_code=400, detail="Token ya utilizado")

    return token

@router.get("/validar-publico/{codigo}")
def validar_token_publico(codigo: str, db: Session = Depends(get_db)):

    token = db.query(TokenModel)\
              .filter(TokenModel.Token == codigo)\
              .first()

    if not token:
        return {"valid": False}

    if token.Concretado:
        return {"valid": False}

    return {
        "valid": True,
        "show_video": token.ShowVideo,
        "show_infografia": token.ShowInfografia,
        "show_terms": token.ShowTerms,
        "video_url": None,
        "infografia_url": None,
        "terms_text": "Acepto normas de seguridad"
    }