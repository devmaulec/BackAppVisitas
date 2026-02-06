from pydantic import BaseModel

class PersonalVisitaBase(BaseModel):
    IdVisita: str
    NombreC: str
    NSS: str
    INE: str
    RFC: str
    CURP: str 

class PersonalVisitaCreate(PersonalVisitaBase):
    pass

class PersonalVisitaResponse(PersonalVisitaBase):
    IdPersonalV: int

    class Config:
        orm_mode = True