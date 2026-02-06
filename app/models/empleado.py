from sqlalchemy import Column,Integer, String
from app.core.database import Base

class Empleado(Base):
    __tablename__ = "empleado"

    IdEmpleado = Column(Integer, primary_key=True, index=True)
    MailEmpleado = Column(String(60), nullable=False)
    NombreEmpleado = Column(String(60), nullable=False)