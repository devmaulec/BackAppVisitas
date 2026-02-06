from pydantic import BaseModel

class VisitaBase(BaseModel):
    NombreProveedor: str
    Ubicacion: str
    RFC: str
    IdTipoV: int

class VisitaCreate(VisitaBase):
    pass

class VisitaResponse(VisitaBase):
    IdVisita: int

    class Config:
        orm_mode = True