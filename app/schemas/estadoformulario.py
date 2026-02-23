from pydantic import BaseModel

class EstadoFormularioBase(BaseModel):
    IdTipoMulti: int
    IdToken: int
    EstadoFormulario: bool 

class EstadoFormularioCreate(EstadoFormularioBase):
    pass

class EstadoFormularioResponse(EstadoFormularioBase):
    IdEstadoFormulario: int

    class Config:
        orm_mode = True