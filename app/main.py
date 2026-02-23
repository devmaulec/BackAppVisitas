import token
from fastapi import FastAPI, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.routers import formulario, invitacion, tokens, acceso
from app.routers import validacion
from .core.config import settings
from app.core.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from app.core.deps import get_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # para pruebas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(tokens.router)
app.include_router(invitacion.router)
app.include_router(formulario.router)
# app.include_router(formulario.router)
# app.include_router(personal_visita.router)
# app.include_router(validacion.router)
app.include_router(acceso.router)
