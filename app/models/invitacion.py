from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base 

class Invitacion(Base):
    __tablename__="Invitacion"

    IdInvitacion = Column(Integer, primary_key=True, index=True)
    NombreProveedor = Column(String(60), nullable=False)
    Procedencia = Column(String(60), nullable=False)
    RFC = Column(String(60), nullable=False)
    Correo = Column(String(60), nullable=False)
    IdTipoVisita = Column(Integer, ForeignKey("TipoVisita.IdTipoVisita"), nullable=False)
    Herramienta = Column(String(255))