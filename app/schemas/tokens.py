from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TokenBase(BaseModel):
    IdInvitacion: int
    IdEmpleado: int
    Concretado: bool = False
    
class TokenCreate(TokenBase):
   pass

class TokenResponse(BaseModel):
    IdToken: int
    Token: str

    class Config:
        orm_mode = True