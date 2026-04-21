from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.schemas.tokens import TokenCreate, TokenResponse
from app.utils.token_generador import generar_token_unico

router = APIRouter(prefix="/tokens", tags=["Token"])

@router.post("/", response_model=TokenResponse)
def crear_token(data: TokenCreate, db: Session = Depends(get_db)):

    token_generado = generar_token_unico(db)

    db.execute(
        text("""
            INSERT INTO Tokens (IdInvitacion, IdEmpleado, Token, Concretado)
            VALUES (:id_invitacion, :id_empleado, :token, false)
        """),
        {
            "id_invitacion": data.IdInvitacion,
            "id_empleado": data.IdEmpleado,
            "token": token_generado
        }
    )
    db.commit()

    id_token = db.execute(
        text("SELECT LAST_INSERT_ID()")
    ).scalar()

    nuevo_token = db.execute(
        text("""
            SELECT 
                IdToken,
                IdInvitacion,
                IdEmpleado,
                Token,
                Concretado
            FROM Tokens
            WHERE IdToken = :id_token
        """),
        {"id_token": id_token}
    ).fetchone()

    return TokenResponse.model_validate(nuevo_token)

@router.get("/prevista/{token}")
def prevista(token: str, db: Session = Depends(get_db)):

    estados = db.execute(
        text("""
            SELECT 
                ef.EstadoFormulario,
                tm.Descripcion
            FROM EstadoFormulario ef
            JOIN TipoMultimedia tm 
              ON tm.IdTipoMulti = ef.IdTipoMulti
            WHERE ef.IdToken = :token
        """),
        {"token": token}
    ).fetchall()

    response = {
        "showVideo": False,
        "showInfografia": False,
        "showTerms": False,
        "videoUrl": None,
        "infografiaUrl": None,
        "termsText": None
    }

    for e in estados:
        if e.Descripcion == "VIDEO":
            response["showVideo"] = bool(e.EstadoFormulario)
        elif e.Descripcion == "INFOGRAFIA":
            response["showInfografia"] = bool(e.EstadoFormulario)
        elif e.Descripcion == "TERMINOS":
            response["showTerms"] = bool(e.EstadoFormulario)
            response["termsText"] = "Acepto normas de seguridad"

    return response

@router.get("/estado/{token}")
def estado_token(token: str, db: Session = Depends(get_db)):

    token_row = db.execute(
        text("""
            SELECT IdToken
            FROM tokens
            WHERE Token = :token
            LIMIT 1
        """),
        {"token": token}
    ).fetchone()

    if not token_row:
        raise HTTPException(status_code=404, detail="Token no encontrado")

    id_token = token_row.IdToken

    total = db.execute(
        text("""
            SELECT COUNT(IdFormulario)
            FROM relacion
            WHERE IdToken = :id_token
        """),
        {"id_token": id_token}
    ).scalar()

    completed = db.execute(
        text("""
            SELECT COUNT(IdEstadoFormulario)
            FROM estadoformulario
            WHERE IdToken = :id_token
              AND EstadoFormulario = 1
        """),
        {"id_token": id_token}
    ).scalar()

    return {
        "valid": True,
        "total": total or 0,
        "completed": completed or 0
    }