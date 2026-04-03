from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from app.core.database import Base

class TipoVisita(Base):
    __tablename__="tipovisita"
 
    IdTipoVisita = Column(Integer, primary_key=True, index=True)
    Descripcion = Column(String(20), nullable=False)
 
    documentos = relationship("TipoVisitaTipoDoc", back_populates="tipo_visita")