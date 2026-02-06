from pydantic import BaseModel

class RelacionCreate(BaseModel):
    IdVisita: int
    IdPersonalV: int
    IdToken: int

class RelacionResponse(RelacionCreate):
    IdRelacion: int

    class Config:
        orm_mode = True