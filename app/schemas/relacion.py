from pydantic import BaseModel

class RelacionBase(BaseModel):
    IdInvitacion: int
    IdFormulario: int
    IdToken: int
    IdTipoMulti: int
    IdTipoDoc: int

class RelacionCreate(RelacionBase):
    pass

    class Config:
        orm_mode = True