from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base 

class Visita(Base):
    __tablename__="visitas"

    IdVisita = Column(Integer, primary_key=True, index=True)
    NombreProveedor = Column(String(60), nullable=False)
    Ubicacion = Column(String(60), nullable=False)
    RFC = Column(String(60), nullable=False)
    IdTipoV = Column(Integer, ForeignKey("tipov.IdTipoV"), nullable=False)