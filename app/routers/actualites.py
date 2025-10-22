from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Actualites
from app.schemas import ActualiteCreate

router = APIRouter(prefix="/api/actualites", tags=["Actualités"])


@router.post("/")
async def create_actualite(actualite: ActualiteCreate, db: Session = Depends(get_db)):
    db_actualite = Actualites(**actualite.dict())
    db.add(db_actualite)
    db.commit()
    db.refresh(db_actualite)
    return db_actualite


@router.get("/")
async def get_actualites(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    actualites = db.query(Actualites).offset(skip).limit(limit).all()
    return actualites


@router.get("/{actualite_id}")
async def get_actualite(actualite_id: int, db: Session = Depends(get_db)):
    actualite = db.query(Actualites).filter(Actualites.id_actualite == actualite_id).first()
    if not actualite:
        raise HTTPException(status_code=404, detail="Actualité non trouvée")
    return actualite


@router.put("/{actualite_id}")
async def update_actualite(actualite_id: int, actualite: ActualiteCreate, db: Session = Depends(get_db)):
    db_actualite = db.query(Actualites).filter(Actualites.id_actualite == actualite_id).first()
    if not db_actualite:
        raise HTTPException(status_code=404, detail="Actualité non trouvée")

    for key, value in actualite.dict().items():
        setattr(db_actualite, key, value)

    db.commit()
    db.refresh(db_actualite)
    return db_actualite


@router.delete("/{actualite_id}")
async def delete_actualite(actualite_id: int, db: Session = Depends(get_db)):
    actualite = db.query(Actualites).filter(Actualites.id_actualite == actualite_id).first()
    if not actualite:
        raise HTTPException(status_code=404, detail="Actualité non trouvée")

    db.delete(actualite)
    db.commit()
    return {"message": "Actualité supprimée avec succès"}