from pydantic import BaseModel
from typing import List

class DocumentoCreate(BaseModel):
    IdTipoDoc: int
    Documento: str

class FormularioBase(BaseModel):
    IdInvitacion: int

class FormularioCreate(FormularioBase):
    NombreC: str
    Documentos: List[DocumentoCreate]

class FormularioResponse(FormularioBase):
    IdFormulario: int
    NombreC: str

    class Config:
        orm_mode = True