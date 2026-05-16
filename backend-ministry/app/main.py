# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialisation de l'application FastAPI
app = FastAPI(
    title="EduSync Ministry API",
    description="API de synchronisation pour le Ministère de l'Enseignement",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ✅ Middleware CORS (Autoriser le frontend React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],  # URL de votre frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Import et inclusion des Routers
from app.api.v1 import auth, sync

app.include_router(auth.router, tags=["Authentication"])

app.include_router(sync.router, prefix="/api/v1/sync", tags=["Synchronization"])

# ✅ Endpoint de vérification (Health Check)
@app.get("/")
async def root():
    return {
        "message": "EduSync Ministry API is running",
        "status": "healthy",
        "docs": "/docs"
    }