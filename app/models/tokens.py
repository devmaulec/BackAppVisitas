from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean, String
from app.core.database import Base

class Token(Base):
    __tablename__="tokens"

    IdToken = Column(Integer, primary_key=True, index=True, autoincrement=True)
    IdInvitacion = Column(Integer, ForeignKey("Invitacion.IdInvitacion"), nullable=False)
    IdEmpleado = Column(Integer, ForeignKey("empleado.IdEmpleado"), nullable=False)
    Token = Column(String(12), unique=True, nullable=False)
    FechaHoraEntrada = Column(DateTime, nullable=True)
    FechaHoraSalida = Column(DateTime, nullable=True)
    Concretado = Column(Boolean, default=False, nullable=False)