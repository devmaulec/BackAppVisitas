from pydantic import BaseModel

class FormularioVisita(BaseModel):

    token: str

    NombreVisitante: str
    Empresa: str

    IdEmpleado: int

    TipoFormulario: str

    Producto: str | None = None
    Asunto: str | None = None
    Motivo: str | None = None