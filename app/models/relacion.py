from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base

class Relacion(Base):
    __tablename__="relacion"

    IdRelacion = Column(Integer, primary_key=True)
    IdVisita = Column(Integer, ForeignKey("visitas.IdVisita"), nullable=False)
    IdPersonalV = Column(Integer, ForeignKey("personalvisita.IdPersonalV"), nullable=False)
    IdToken = Column(Integer,ForeignKey("tokens.IdToken"), nullable=False)