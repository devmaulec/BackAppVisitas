from sqlalchemy import Integer, String, Column, ForeignKey
from app.core.database import Base

class FormDocs(Base):
    __tablename__ = "FormDocs"

    IdFormDocs = Column(Integer, primary_key=True, index=True, autoincrement=True)
    IdFormulario = Column(Integer, ForeignKey("Formulario.IdFormulario"))
    IdTipoDoc = Column(Integer, ForeignKey("TipoDoc.IdTipoDoc"))
    Documento = Column(String(255))
    Ruta = Column(String(255))