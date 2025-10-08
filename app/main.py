# app/main.py

# app/main.py

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import timedelta
import os
import uuid
import shutil
from dotenv import load_dotenv
from typing import List

# Importations des composants locaux
from app.database import engine, Base, get_db
from app.models import Admin, Formations, Actualites
from app.schemas import AdminCreate, AdminResponse, AdminUpdate, FormationCreate, ActualiteCreate
# Nous importons le routeur ici
from app.auth import get_password_hash, create_access_token, get_current_admin, ACCESS_TOKEN_EXPIRE_MINUTES, router as auth_router

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

# 🚨 CORRECTION CRUCIALE : Inclusion du routeur d'authentification
app.include_router(
    auth_router,
    prefix="/api/auth",
    tags=["Auth"]
)
# --------------------------------------------------------------------------------------

## Gestion de l'Admin par Défaut et Démarrage

# Créer un admin par défaut au démarrage
def create_default_admin(db: Session):
    """Créer un administrateur par défaut si aucun n'existe"""
    try:
        admin_count = db.query(Admin).count()
        if admin_count == 0:
            print("👤 Création de l'admin par défaut...")
            # Mot de passe court pour éviter les problèmes de longueur bcrypt (> 72 bytes)
            hashed_password = get_password_hash("admin123") 
            default_admin = Admin(
                nom="Administrateur Principal",
                email="admin@ecat-taratra.mg",
                password_hash=hashed_password,
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
    # Nécessite un next() car get_db est un générateur
    try:
        db = next(get_db()) 
        create_default_admin(db)
    except Exception as e:
        print(f"❌ ERREUR DE BASE DE DONNÉES au démarrage : {e}")


# --------------------------------------------------------------------------------------
## Routes Administrateurs

# Route pour récupérer l'admin connecté
@app.get("/api/admins/me", response_model=AdminResponse)
async def get_current_admin_endpoint(current_admin: Admin = Depends(get_current_admin)):
    """
    Récupérer les informations de l'administrateur connecté (nécessite un token Bearer)
    """
    return current_admin

@app.post("/api/admins", response_model=AdminResponse, status_code=status.HTTP_201_CREATED)
async def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    existing_admin = db.query(Admin).filter(Admin.email == admin.email).first()
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un administrateur avec cet email existe déjà"
        )
        
    hashed_password = get_password_hash(admin.password)
    
    db_admin = Admin(
        nom=admin.nom,
        email=admin.email,
        password_hash=hashed_password
        
    )
    
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

@app.get("/api/admins", response_model=List[AdminResponse])
async def get_admins(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    admins = db.query(Admin).offset(skip).limit(limit).all()
    return admins

@app.get("/api/admins/{admin_id}", response_model=AdminResponse)
async def get_admin(admin_id: int, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.id_admin == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Administrateur non trouvé")
    return admin

@app.put("/api/admins/{admin_id}", response_model=AdminResponse)
async def update_admin(
    admin_id: int, 
    admin_update: AdminUpdate, 
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    db_admin = db.query(Admin).filter(Admin.id_admin == admin_id).first()
    if not db_admin:
        raise HTTPException(status_code=404, detail="Administrateur non trouvé")
    
    if admin_update.email:
        existing_admin = db.query(Admin).filter(
            Admin.email == admin_update.email,
            Admin.id_admin != admin_id
        ).first()
        if existing_admin:
            raise HTTPException(
                status_code=400,
                detail="Un administrateur avec cet email existe déjà"
            )
    
    update_data = admin_update.dict(exclude_unset=True)
    
    if 'password' in update_data and update_data['password']:
        update_data['password_hash'] = get_password_hash(update_data['password'])
        del update_data['password']
    
    for key, value in update_data.items():
        setattr(db_admin, key, value)
    
    db.commit()
    db.refresh(db_admin)
    return db_admin

@app.delete("/api/admins/{admin_id}")
async def delete_admin(
    admin_id: int, 
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    admin = db.query(Admin).filter(Admin.id_admin == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Administrateur non trouvé")
    
    total_admins = db.query(Admin).count()
    if total_admins <= 1:
        raise HTTPException(
            status_code=400,
            detail="Impossible de supprimer le dernier administrateur"
        )
    
    db.delete(admin)
    db.commit()
    return {"message": "Administrateur supprimé avec succès"}

# --------------------------------------------------------------------------------------
## Routes Uploads et Contenu

@app.post("/api/upload/image")
async def upload_image(file: UploadFile = File(...)):
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Le fichier doit être une image")
        
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
        filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        image_url = f"http://localhost:5000/uploads/{filename}"
        
        return {
            "filename": filename, 
            "url": image_url,
            "message": "Upload réussi"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'upload: {str(e)}")

# Routes pour les formations (correctes)

@app.post("/api/formations")
async def create_formation(formation: FormationCreate, db: Session = Depends(get_db)):
    db_formation = Formations(**formation.dict())
    db.add(db_formation)
    db.commit()
    db.refresh(db_formation)
    return db_formation

@app.get("/api/formations")
async def get_formations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    formations = db.query(Formations).offset(skip).limit(limit).all()
    return formations

@app.get("/api/formations/{formation_id}")
async def get_formation(formation_id: int, db: Session = Depends(get_db)):
    formation = db.query(Formations).filter(Formations.id_formation == formation_id).first()
    if not formation:
        raise HTTPException(status_code=404, detail="Formation non trouvée")
    return formation

@app.put("/api/formations/{formation_id}")
async def update_formation(formation_id: int, formation: FormationCreate, db: Session = Depends(get_db)):
    db_formation = db.query(Formations).filter(Formations.id_formation == formation_id).first()
    if not db_formation:
        raise HTTPException(status_code=404, detail="Formation non trouvée")
    
    for key, value in formation.dict().items():
        setattr(db_formation, key, value)
    
    db.commit()
    db.refresh(db_formation)
    return db_formation

@app.delete("/api/formations/{formation_id}")
async def delete_formation(formation_id: int, db: Session = Depends(get_db)):
    formation = db.query(Formations).filter(Formations.id_formation == formation_id).first()
    if not formation:
        raise HTTPException(status_code=404, detail="Formation non trouvée")
    
    db.delete(formation)
    db.commit()
    return {"message": "Formation supprimée avec succès"}

# --------------------------------------------------------------------------------------
# Routes pour les actualités (correctes)

@app.post("/api/actualites")
async def create_actualite(actualite: ActualiteCreate, db: Session = Depends(get_db)):
    db_actualite = Actualites(**actualite.dict())
    db.add(db_actualite)
    db.commit()
    db.refresh(db_actualite)
    return db_actualite

@app.get("/api/actualites")
async def get_actualites(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    actualites = db.query(Actualites).offset(skip).limit(limit).all()
    return actualites

@app.get("/api/actualites/{actualite_id}")
async def get_actualite(actualite_id: int, db: Session = Depends(get_db)):
    actualite = db.query(Actualites).filter(Actualites.id_actualite == actualite_id).first()
    if not actualite:
        raise HTTPException(status_code=404, detail="Actualité non trouvée")
    return actualite

@app.put("/api/actualites/{actualite_id}")
async def update_actualite(actualite_id: int, actualite: ActualiteCreate, db: Session = Depends(get_db)):
    db_actualite = db.query(Actualites).filter(Actualites.id_actualite == actualite_id).first()
    if not db_actualite:
        raise HTTPException(status_code=404, detail="Actualité non trouvée")
    
    for key, value in actualite.dict().items():
        setattr(db_actualite, key, value)
    
    db.commit()
    db.refresh(db_actualite)
    return db_actualite

@app.delete("/api/actualites/{actualite_id}")
async def delete_actualite(actualite_id: int, db: Session = Depends(get_db)):
    actualite = db.query(Actualites).filter(Actualites.id_actualite == actualite_id).first()
    if not actualite:
        raise HTTPException(status_code=404, detail="Actualité non trouvée")
    
    db.delete(actualite)
    db.commit()
    return {"message": "Actualité supprimée avec succès"}

# --------------------------------------------------------------------------------------
### Routes de Base

@app.get("/")
async def root():
    return {"message": "API ECAT TARATRA"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
