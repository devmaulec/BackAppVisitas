from pydantic import BaseModel

class InvitacionBase(BaseModel):
    NombreProveedor: str
    Procedencia: str
    Correo: str
    RFC: str
    IdTipoVisita: int
    Herramienta: str

class InvitacionCreate(InvitacionBase):
    pass

class InvitacionResponse(InvitacionBase):
    IdInvitacion: int

    class Config:
        orm_mode = True