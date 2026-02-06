from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.tokens import Token
from datetime import datetime

router = APIRouter(prefix="/validacion", tags=["Validacion"])

@router.get("/{token}")
def validar_qr(token: int, db: Session = Depends(get_db)):
    token_db = db.query(Token).filter(Token.IdToken == token).first()

    if not token_db:
        raise HTTPException(status_code=404, detail="Token inválido")

    token_db.FechaHoraEntrada = datetime.now()
    token_db.Conectado = 1

    db.commit()

    return {
        "permitido": True,
        "token": token,
        "entrada": token_db.FechaHoraEntrada
    }