from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
 
from app.models import (
    empleado,
    tipo_visita_tipodoc,
    estadoformulario,
    formdocs,
    formulario as formulario_model,
    invitacion as invitacion_model,
    relacion,
    tipo_visita,
    tipodoc,
    tipomutimedia,
    tokens as tokens_model
)
from app.routers import formulario as formulario_router
from app.routers import invitacion as invitacion_router
from app.routers import tokens as tokens_router
from app.routers import acceso
 
app = FastAPI()
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
Base.metadata.create_all(bind=engine)
 
app.include_router(tokens_router.router)
app.include_router(invitacion_router.router)
app.include_router(formulario_router.router)
app.include_router(acceso.router)