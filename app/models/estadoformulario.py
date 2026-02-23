from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from app.core.database import Base

class EstadoFormulario(Base):
    __tablename__ = "EstadoFormulario"

    IdEstadoFormulario = Column(Integer, primary_key=True, index=True)
    IdTipoMulti = Column(Integer, ForeignKey("TipoMultimedia.IdTipoMulti"), nullable=False)
    IdToken = Column(Integer, ForeignKey("tokens.IdToken"), nullable=False)
    EstadoFormulario = Column(Boolean)
