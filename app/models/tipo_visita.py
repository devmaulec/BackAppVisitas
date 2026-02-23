from sqlalchemy import Column, ForeignKey, String, Integer
from app.core.database import Base

class TipoVisita(Base):
    __tablename__="TipoVisita"

    IdTipoVisita = Column(Integer, primary_key=True, index=True)
    Descripcion = Column(String(20), nullable=False)
    IdTipoDoc = Column(Integer, ForeignKey("TipoDoc.IdTipoDoc"))
