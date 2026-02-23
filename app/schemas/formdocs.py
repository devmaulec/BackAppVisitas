from pydantic import BaseModel

class FormDocBase(BaseModel):
    IdFormulario: int
    IdTipodOC: int
    Documento: str
    Ruta: str

class FormDocCreate(FormDocBase):
    pass

class FormDocResponse(FormDocBase):
    IdFormsDocs:int

    class Config:
        orm_mode = True