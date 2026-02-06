from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TokenCreate(BaseModel):
    IdVisita: int
    IdEmpleado: int

class TokenResponse(BaseModel):
    IdToken: int
    IdVisita: int
    IdEmpleado: int
    ShowVideo: bool
    ShowInfografia: bool
    ShowTerms: bool
    FechaHoraEntrada: Optional[datetime]
    FechaHoraSalida: Optional[datetime]
    Concretado: bool

    class Config:
        orm_mode = True