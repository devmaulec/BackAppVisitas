from sqlalchemy import Column, String, Integer
from app.core.database import Base

class TipoVisita(Base):
    __tablename__="tipov"

    IdTipoV = Column(Integer, primary_key=True, index=True)
    Descripcion = Column(String(20),nullable=False)
    