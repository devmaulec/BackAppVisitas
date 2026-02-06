from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean, String
from app.core.database import Base

class Token(Base):
    __tablename__="tokens"

    IdToken = Column(Integer, primary_key=True, index=True)
    IdVisita = Column(Integer, ForeignKey("visitas.IdVisita"), nullable=False)
    IdEmpleado = Column(Integer, ForeignKey("empleado.IdEmpleado"), nullable=False)
    Token = Column(String(13), unique=True, nullable=False)

    ShowVideo = Column(Boolean, default=False, nullable=False)  
    ShowInfografia = Column(Boolean, default=False, nullable=False)  
    ShowTerms = Column(Boolean, default=False, nullable=False)  

    FechaHoraEntrada = Column(DateTime, nullable=True)
    FechaHoraSalida = Column(DateTime, nullable=True)

    FormularioCompleto = Column(Boolean, default=False, nullable=False)  # 👈 AQUI
    Concretado = Column(Boolean, default=False, nullable=False)