from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.deps import get_db
from app.models.tokens import Token

router = APIRouter(prefix="/acceso", tags=["Acceso"])

@router.post("/entrada/{token}")
def registrar_entrada(token: int, db: Session = Depends(get_db)):

    token_db = db.query(Token).filter(Token.IdToken == token).first()

    if not token_db:
        raise HTTPException(status_code=404, detail="Token inválido")

    token_db.FechaHoraEntrada = datetime.now()
    token_db.Conectado = 1

    db.commit()

    return {"mensaje": "Entrada autorizada"}


@router.post("/salida/{token}")
def registrar_salida(token: int, db: Session = Depends(get_db)):

    token_db = db.query(Token).filter(Token.IdToken == token).first()

    if not token_db:
        raise HTTPException(status_code=404, detail="Token inválido")

    token_db.FechaHoraSalida = datetime.now()

    db.commit()

    return {"mensaje": "Salida registrada"}