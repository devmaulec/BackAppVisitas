from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class PersonalVisita(Base):
    __tablename__="personalvisita"

    IdPersonalV = Column(Integer, primary_key=True, index=True)
    IdVisita = Column(Integer, ForeignKey("visitas.IdVisita"), nullable=False)
    NombreC = Column(String(60), nullable=False)
    NSS = Column(String(11), nullable=False)
    INE = Column(String(20), nullable=False)
    RFC = Column(String(13), nullable=False)
    CURP = Column(String(18), nullable=False)