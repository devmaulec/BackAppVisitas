from sqlalchemy import Column, Integer, String
from app.core.database import Base

class TipoMultimedia(Base):
    __tablename__ = "TipoMultimedia"

    IdTipoMulti = Column(Integer, primary_key=True, index=True)
    Descripcion = Column(String(255))