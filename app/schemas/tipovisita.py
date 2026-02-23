from pydantic import BaseModel

class TipoVisitaBase(BaseModel):
    Descripcion:str

class TipoVisitaCreate(TipoVisitaBase):
    pass

class TipoVisitaResponse(BaseModel):
    IdTipoV: int

    class Config: 
        orm_mode = True