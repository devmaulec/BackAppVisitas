from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
 
from app.core.deps import get_db
from app.models.formdocs import FormDocs
from app.models.formulario import Formulario
from app.models.invitacion import Invitacion
from app.models.tipodoc import TipoDoc
from app.models.tokens import Token
from app.models.tipo_visita_tipodoc import TipoVisitaTipoDoc
 
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
        .join(TipoVisitaTipoDoc, TipoVisitaTipoDoc.IdTipoDoc == TipoDoc.IdTipoDoc)\
        .filter(TipoVisitaTipoDoc.IdTipoVisita == invitacion.IdTipoVisita)\
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
 
    nuevo_formulario = Formulario(
        NombreC=data.NombreC,
        IdInvitacion=token_db.IdInvitacion
    )
 
    db.add(nuevo_formulario)
    db.commit()
    db.refresh(nuevo_formulario)
 
    return {
        "mensaje": "Formulario creado correctamente",
        "IdFormulario": nuevo_formulario.IdFormulario
    }

@router.post("/{id_formulario}/documentos")
def subir_documentos(
    id_formulario: int,
    data: FormularioCreate,
    db: Session = Depends(get_db)
):
    try:
        formulario = db.query(Formulario)\
            .filter(Formulario.IdFormulario == id_formulario)\
            .first()
 
        if not formulario:
            raise HTTPException(status_code=404, detail="Formulario no encontrado")

        invitacion = db.query(Invitacion)\
            .filter(Invitacion.IdInvitacion == formulario.IdInvitacion)\
            .first()
 
        if not invitacion:
            raise HTTPException(status_code=404, detail="Invitación no encontrada")
 
        docs_validos = db.query(TipoVisitaTipoDoc)\
            .filter(TipoVisitaTipoDoc.IdTipoVisita == invitacion.IdTipoVisita)\
            .all()
 
        ids_validos = [d.IdTipoDoc for d in docs_validos]
 
        for doc in data.Documentos:
 
            if doc.IdTipoDoc not in ids_validos:
                raise HTTPException(
                    status_code=400,
                    detail=f"Documento {doc.IdTipoDoc} no permitido para este tipo de visita"
                )
 
            nuevo_doc = FormDocs(
                IdFormulario=id_formulario,
                IdTipoDoc=doc.IdTipoDoc,
                Documento=doc.Documento,
                Ruta=f"uploads/{doc.Documento}"
            )
 
            db.add(nuevo_doc)
 
        db.commit()
 
        return {
            "mensaje": "Documentos guardados correctamente"
        }
 
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al guardar documentos: {str(e)}"
        )