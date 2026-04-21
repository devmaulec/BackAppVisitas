from pydantic import BaseModel
from typing import List

class FormularioCreate(BaseModel):
    NombreC: str

class DocumentoCreate(BaseModel):
    IdTipoDoc: int
    Documento: str


class DocumentosRequest(BaseModel):
    Documentos:List[DocumentoCreate]

    class Config:
        orm_mode = True