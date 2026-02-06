from pydantic import BaseModel

class EmpleadoBase(BaseModel):
    MailEmpleado: str
    NombreEmpleado: str

class EmpleadoResponse(EmpleadoBase):
    IdEmpleado: int

    class Config:
        orm_mode = True