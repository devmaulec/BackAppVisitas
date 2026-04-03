from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class TipoDoc(Base):
    __tablename__= "tipodoc"

    IdTipoDoc = Column(Integer, primary_key=True, index=True)
    Descripcion = Column(String(255))

    tipos_visita = relationship(
        "TipoVisitaTipoDoc",
        back_populates="tipo_doc"
    )