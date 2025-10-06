from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os
import uuid
import shutil
from dotenv import load_dotenv

from app.database import engine, Base, get_db
from app.models import Admin, Formations, Actualites
from app.schemas import AdminCreate, FormationCreate, ActualiteCreate

load_dotenv()

# Créer les tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ECAT TARATRA API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configuration CORS COMPLÈTE
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "http://localhost:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Configuration pour les uploads
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Servir les fichiers statiques
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

@app.post("/api/upload/image")
async def upload_image(file: UploadFile = File(...)):
    try:
        print(f"📤 Upload reçu: {file.filename} ({file.content_type})")
        
        # Validation du type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Le fichier doit être une image")
        
        # Générer un nom unique
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
        filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        print(f"💾 Sauvegarde vers: {file_path}")
        
        # Sauvegarder le fichier
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # URL accessible depuis le frontend
        image_url = f"http://localhost:5000/uploads/{filename}"
        print(f"🔗 URL générée: {image_url}")
        
        return {
            "filename": filename, 
            "url": image_url,
            "message": "Upload réussi"
        }
        
    except Exception as e:
        print(f"❌ Erreur upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'upload: {str(e)}")

# Routes pour les formations
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

# Routes pour les actualités
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

# Routes de base
@app.get("/")
async def root():
    return {"message": "API ECAT TARATRA"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Route de debug pour les uploads
@app.get("/api/debug/uploads")
async def list_uploaded_files():
    files = []
    for filename in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, filename)
        if os.path.isfile(file_path):
            files.append({
                "name": filename,
                "size": os.path.getsize(file_path),
                "url": f"http://localhost:5000/uploads/{filename}"
            })
    return {"upload_dir": UPLOAD_DIR, "files": files}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)