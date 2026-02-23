from sqlalchemy import Column, Integer, String
from app.core.database import Base

class TipoDoc(Base):
    __tablename__= "TipoDoc"

    IdTipoDoc = Column(Integer, primary_key=True, index=True)
    Descripcion = Column(String(255))