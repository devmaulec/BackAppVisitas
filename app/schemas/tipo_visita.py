from pydantic import BaseModel

class TipoVisitaResponse(BaseModel):
    IdTipoV: int
    Descripcion: str

    class Config: 
        orm_mode = True