import token
from fastapi import FastAPI, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.routers import personal_visita, tokens, visitas, acceso
from app.routers import validacion
from .core.config import settings
from .routers import formulario
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
app.include_router(visitas.router)
app.include_router(formulario.router)
app.include_router(personal_visita.router)
app.include_router(validacion.router)
app.include_router(acceso.router)


# @app.get("/validate-token")
# def validate_token(token:str):
#     if token == "TEST123":
#         return{"valid": True}
#     return{"valid": False}




# @app.get("/visits/validate-token")
# def validate_token(token: str):
#     # 🔹 Simulación mientras no hay BD
#     if token != "TEST123":
#         return {
#             "valid": False
#         }

#     return {
#         "valid": True,
#         "show_video": True,
#         "show_infografia": False,
#         "show_terms": True,
#         "video_url": None,          # luego vendrá CDN o S3
#         "infografia_url": None,     # luego vendrá URL real
#         "terms_text": "Acepto normas de seguridad y acceso."
#     }

# @app.post("/visits/register")
# async def register_visit(
#     token: str = Form(...),
#     nombre_completo: str = Form(...),
#     nss: str = Form(...),
#     rfc: str = Form(...),
#     curp: str = Form(...),
#     ine: UploadFile = File(...)
# ):
#     # 🔒 Validar token (temporal)
#     if token != "TEST123":
#         raise HTTPException(status_code=500, detail="Token inválido")

#     # 📂 Guardar archivo (temporal)
#     file_location = f"uploads/{ine.filename}"
#     with open(file_location, "wb") as f:
#         f.write(await ine.read())

#     # 🧠 Aquí luego va BD
#     return {
#         "success": True,
#         "message": "Visita registrada correctamente"
#     }

