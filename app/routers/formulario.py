from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.deps import get_db
from app.models.formdocs import FormDocs
from app.models.formulario import Formulario
from app.models.invitacion import Invitacion
from app.models.tipo_visita import TipoVisita
from app.models.tipodoc import TipoDoc
from app.models.tokens import Token
from app.schemas.formulario import FormularioCreate

router = APIRouter(prefix="/formulario", tags=["Formulario"])

@router.get("/token/{token}")
def obtener_formulario(token: str, db: Session = Depends(get_db)):

    token_db = db.query(Token).filter(Token.Token == token).first()

    if not token_db:
        raise HTTPException(status_code=404, detail="Token inválido")

    invitacion = db.query(Invitacion)\
        .filter(Invitacion.IdInvitacion == token_db.IdInvitacion)\
        .first()

    if not invitacion:
        raise HTTPException(status_code=404, detail="Invitación no encontrada")

    documentos = db.query(TipoDoc)\
        .join(TipoVisita, TipoVisita.IdTipoDoc == TipoDoc.IdTipoDoc)\
        .filter(TipoVisita.IdTipoVisita == invitacion.IdTipoVisita)\
        .all()

    return {
        "IdInvitacion": invitacion.IdInvitacion,
        "TipoVisita": invitacion.IdTipoVisita,
        "CamposBase": {
            "NombreProveedor": invitacion.NombreProveedor,
            "Correo": invitacion.Correo
        },
        "DocumentosRequeridos": [
            {
                "IdTipoDoc": doc.IdTipoDoc,
                "Descripcion": doc.Descripcion
            }
            for doc in documentos
        ]
    }

@router.post("/crear/{token}")
def crear_formulario(
    token: str,
    data: FormularioCreate,
    db: Session = Depends(get_db)
):
    try:

        token_db = db.query(Token).filter(Token.Token == token).first()

        if not token_db:
            raise HTTPException(status_code=404, detail="Token inválido")

        if token_db.Concretado:
            raise HTTPException(status_code=400, detail="Este token ya fue utilizado")

        ahora = datetime.now()

        if token_db.FechaHoraEntrada and ahora < token_db.FechaHoraEntrada:
            raise HTTPException(status_code=400, detail="El token aún no está activo")

        if token_db.FechaHoraSalida and ahora > token_db.FechaHoraSalida:
            raise HTTPException(status_code=400, detail="El token ya expiró")

        # Crear formulario
        nuevo_formulario = Formulario(
            NombreC=data.NombreC
        )

        db.add(nuevo_formulario)
        db.flush() 

        for doc in data.Documentos:
            form_doc = FormDocs(
                IdFormulario=nuevo_formulario.IdFormulario,
                IdTipoDoc=doc.IdTipoDoc,
                Documento=doc.Documento,
                Ruta=f"uploads/{doc.Documento}"
            )
            db.add(form_doc)

        token_db.Concretado = True

        db.commit()
        db.refresh(nuevo_formulario)

        return {
            "mensaje": "Formulario creado correctamente",
            "IdFormulario": nuevo_formulario.IdFormulario
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al crear el formulario: {str(e)}"
        )