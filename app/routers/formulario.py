from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime

from app.core.deps import get_db
from app.schemas.formulario import DocumentosRequest, FormularioCreate

router = APIRouter(prefix="/formulario", tags=["Formulario"])

@router.post("/crear/{token}")
def crear_formulario(
    token: str,
    data: FormularioCreate,
    db: Session = Depends(get_db)
):

    token_db = db.execute(
        text("""
            SELECT *
            FROM tokens
            WHERE Token = :token
            LIMIT 1
        """),
        {"token": token}
    ).fetchone()

    if not token_db:
        raise HTTPException(status_code=404, detail="Token inválido")

    if token_db.Concretado:
        raise HTTPException(status_code=400, detail="Este token ya fue utilizado")

    ahora = datetime.now()

    if token_db.FechaHoraEntrada and ahora < token_db.FechaHoraEntrada:
        raise HTTPException(status_code=400, detail="El token aún no está activo")

    if token_db.FechaHoraSalida and ahora > token_db.FechaHoraSalida:
        raise HTTPException(status_code=400, detail="El token ya expiró")

    db.execute(
        text("""
            INSERT INTO formulario (NombreC, IdInvitacion)
            VALUES (:nombre, :id_invitacion)
        """),
        {
            "nombre": data.NombreC,
            "id_invitacion": token_db.IdInvitacion
        }
    )
    db.commit()

    id_formulario = db.execute(
        text("SELECT LAST_INSERT_ID()")
    ).scalar()

    return {
        "mensaje": "Formulario creado",
        "IdFormulario": id_formulario
    }

@router.post("/{id_formulario}/documentos")
def subir_documentos(
    id_formulario: int,
    data: DocumentosRequest,
    db: Session = Depends(get_db)
):

    formulario = db.execute(
        text("""
            SELECT *
            FROM formulario
            WHERE IdFormulario = :id_formulario
            LIMIT 1
        """),
        {"id_formulario": id_formulario}
    ).fetchone()

    if not formulario:
        raise HTTPException(status_code=404, detail="Formulario no encontrado")

    invitacion = db.execute(
        text("""
            SELECT *
            FROM invitacion
            WHERE IdInvitacion = :id_invitacion
            LIMIT 1
        """),
        {"id_invitacion": formulario.IdInvitacion}
    ).fetchone()

    if not invitacion:
        raise HTTPException(status_code=404, detail="Invitación no encontrada")

    docs_validos = db.execute(
        text("""
            SELECT IdTipoDoc
            FROM tipo_visita_tipodoc
            WHERE IdTipoVisita = :id_tipo_visita
        """),
        {"id_tipo_visita": invitacion.IdTipoVisita}
    ).fetchall()

    ids_validos = [d.IdTipoDoc for d in docs_validos]
    ids_enviados = [doc.IdTipoDoc for doc in data.Documentos]

    faltantes = set(ids_validos) - set(ids_enviados)
    if faltantes:
        raise HTTPException(
            status_code=400,
            detail=f"Faltan documentos requeridos: {list(faltantes)}"
        )

    for doc in data.Documentos:
        if doc.IdTipoDoc not in ids_validos:
            raise HTTPException(
                status_code=400,
                detail=f"Documento {doc.IdTipoDoc} no permitido"
            )

    for doc in data.Documentos:
        db.execute(
            text("""
                INSERT INTO formdocs (IdFormulario, IdTipoDoc, Documento, Ruta)
                VALUES (:id_formulario, :id_tipo_doc, :documento, :ruta)
            """),
            {
                "id_formulario": id_formulario,
                "id_tipo_doc": doc.IdTipoDoc,
                "documento": doc.Documento,
                "ruta": f"uploads/{doc.Documento}"
            }
        )

    db.commit()

    return {
        "mensaje": "Documentos guardados correctamente"
    }