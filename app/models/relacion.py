from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base

class Relacion(Base):
    __tablename__="relacion"

    IdRelacion = Column(Integer, primary_key=True)
    IdInvitacion = Column(Integer, ForeignKey("Invitados.IdInvitados"), nullable=False)
    IdFormulario = Column(Integer, ForeignKey("Formulario.IdFormulario"), nullable=False)
    IdToken = Column(Integer,ForeignKey("tokens.IdToken"), nullable=False)
    IdTipoMulti = Column(Integer, ForeignKey("TipoMultimedia.IdTipoMulti"))
    IdTipoDoc = Column(Integer, ForeignKey("TipoDoc.IdTipoDoc"))