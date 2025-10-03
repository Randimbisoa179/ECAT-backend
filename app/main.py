from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.routes import admin, formations, actualites
from app.database import engine, Base, get_db
from app.models import Admin
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="ECAT TARATRA API",
    description="API pour le site vitrine ECAT TARATRA avec Neon PostgreSQL",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ "http://localhost:3000",  # Next.js en développement
        "http://127.0.0.1:3000",
        "https://votre-domaine.vercel.app", ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(formations.router, prefix="/api/formations", tags=["Formations"])
app.include_router(actualites.router, prefix="/api/actualites", tags=["Actualités"])


@app.on_event("startup")
async def startup_event():
    """Initialiser la base de données au démarrage"""
    try:
        # Créer les tables
        Base.metadata.create_all(bind=engine)
        print("✅ Base de données connectée avec succès")
    except Exception as e:
        print(f"❌ Erreur de connexion à la base de données: {e}")


@app.get("/")
async def root():
    return {
        "message": "API ECAT TARATRA",
        "database": "Neon PostgreSQL",
        "status": "running"
    }


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Vérifier la santé de l'API et de la base de données"""
    try:
        # Tester la connexion à la base de données
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return {
        "status": "healthy",
        "database": db_status,
        "version": "1.0.0"
    }


@app.get("/test-db")
async def test_db(db: Session = Depends(get_db)):
    """Route de test pour vérifier la connexion à la base de données"""
    try:
        result = db.execute("SELECT version()").fetchone()
        return {
            "status": "success",
            "database_version": result[0],
            "message": "Connexion à Neon PostgreSQL réussie"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Erreur de connexion: {str(e)}"
        }