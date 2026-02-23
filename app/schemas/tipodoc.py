from pydantic import BaseModel

class TipoDocBase(BaseModel):
    Descripcion: str

class TipoDocCreate(TipoDocBase):
    IdTipoDoc: int
    Descripcion: str

class TipoDocResponse(TipoDocBase):
    IdTipoDoc:int

    class config:
        from_attributes = True