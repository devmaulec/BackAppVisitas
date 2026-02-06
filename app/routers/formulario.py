from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.models.tokens import Token
from app.models.visitas import Visita
from app.models.empleado import Empleado
from app.models.personal_visita import PersonalVisita

from app.schemas.formulario import FormularioVisita

router = APIRouter(prefix="/formulario", tags=["Formulario"])

@router.get("/{token}")
def obtener_formulario(token: str, db: Session = Depends(get_db)):

    token_db = db.query(Token)\
                 .filter(Token.Token == token)\
                 .first()

    if not token_db:
        raise HTTPException(status_code=404, detail="Token inválido")

    visita = db.query(Visita)\
               .filter(Visita.IdVisita == token_db.IdVisita)\
               .first()

    empleados = db.query(Empleado).all()

    return {
        "TipoVisita": visita.IdTipoV,
        "Empleados": empleados
    }


@router.put("/")
def guardar_formulario(data: FormularioVisita, db: Session = Depends(get_db)):

    token_db = db.query(Token)\
                 .filter(Token.Token == data.token)\
                 .first()

    if not token_db:
        raise HTTPException(status_code=404, detail="Token inválido")

    visita = db.query(Visita)\
               .filter(Visita.IdVisita == token_db.IdVisita)\
               .first()

    visita.NombreVisitante = data.NombreVisitante
    visita.Empresa = data.Empresa

    relacion = PersonalVisita(
        IdVisita=visita.IdVisita,
        IdEmpleado=data.IdEmpleado
    )

    db.add(relacion)
    db.commit()

    return {"mensaje": "Formulario completado"}