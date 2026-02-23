from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class Formulario(Base):
    __tablename__="Formulario"

    IdFormulario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    IdInvitacion = Column(Integer, ForeignKey("Invitacion.IdInvitacion"), nullable=False)
    NombreC = Column(String(60), nullable=False)