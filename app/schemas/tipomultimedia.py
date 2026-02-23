from pydantic import BaseModel

class TipoMultimediaBase(BaseModel):
    Descripcion: str

class TipoMultimediaCreate(TipoMultimediaBase):
    pass

class TipoMultimediaResponse(TipoMultimediaBase):
    IdTipoMulti: int

    class config:
        from_attributes = True