# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

# Importations des composants locaux
from app.database import engine, Base, get_db
from app.models import Admin
from app.auth import get_password_hash

# Import des routeurs
from app.routers import (
    auth_router,
    admin_router,
    upload_router,
    formations_router,
    actualites_router,
    directors_router,
    about_router,
    contact_info_router,
    contact_messages_router
)

load_dotenv()

# Créer les tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ECAT TARATRA API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# --------------------------------------------------------------------------------------
## Configuration des Middlewares

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Configuration pour les uploads
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# --------------------------------------------------------------------------------------
## Inclusion des routeurs

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(upload_router)
app.include_router(formations_router)
app.include_router(actualites_router)
app.include_router(directors_router)
app.include_router(about_router)
app.include_router(contact_info_router)
app.include_router(contact_messages_router)

# --------------------------------------------------------------------------------------
## Gestion de l'Admin par Défaut et Démarrage

def create_default_admin(db: Session):
    """Créer un administrateur par défaut si aucun n'existe"""
    try:
        admin_count = db.query(Admin).count()
        if admin_count == 0:
            print("👤 Création de l'admin par défaut...")
            hashed_password = get_password_hash("admin123")
            default_admin = Admin(
                nom="Administrateur Principal",
                email="admin@ecat-taratra.mg",
                password_hash=hashed_password,
                role="admin"
            )
            db.add(default_admin)
            db.commit()
            db.refresh(default_admin)
            print("✅ Admin par défaut créé:", default_admin.email)
        else:
            print(f"✅ {admin_count} admin(s) existant(s) dans la base")
    except Exception as e:
        print("❌ Erreur création admin par défaut:", e)

@app.on_event("startup")
async def startup_event():
    try:
        db = next(get_db())
        create_default_admin(db)
    except Exception as e:
        print(f"❌ ERREUR DE BASE DE DONNÉES au démarrage : {e}")

# --------------------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)