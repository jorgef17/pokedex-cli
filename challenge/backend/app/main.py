from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.controllers import note_controller

app = FastAPI()

# Configurar CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde el frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Incluir los controladores
app.include_router(note_controller.router)
