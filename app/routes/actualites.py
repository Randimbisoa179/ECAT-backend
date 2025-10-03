from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Actualites
from app.schemas import ActualiteCreate, ActualiteResponse

router = APIRouter()


@router.post("/", response_model=ActualiteResponse)
def create_actualite(actualite: ActualiteCreate, db: Session = Depends(get_db)):
    db_actualite = Actualites(**actualite.dict())
    db.add(db_actualite)
    db.commit()
    db.refresh(db_actualite)
    return db_actualite


@router.get("/", response_model=List[ActualiteResponse])
def get_actualites(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    actualites = db.query(Actualites).offset(skip).limit(limit).all()
    return actualites


@router.get("/{actualite_id}", response_model=ActualiteResponse)
def get_actualite(actualite_id: int, db: Session = Depends(get_db)):
    actualite = db.query(Actualites).filter(Actualites.id_actualite == actualite_id).first()
    if not actualite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actualité non trouvée"
        )
    return actualite


@router.put("/{actualite_id}", response_model=ActualiteResponse)
def update_actualite(actualite_id: int, actualite: ActualiteCreate, db: Session = Depends(get_db)):
    db_actualite = db.query(Actualites).filter(Actualites.id_actualite == actualite_id).first()
    if not db_actualite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actualité non trouvée"
        )

    for key, value in actualite.dict().items():
        setattr(db_actualite, key, value)

    db.commit()
    db.refresh(db_actualite)
    return db_actualite


@router.delete("/{actualite_id}")
def delete_actualite(actualite_id: int, db: Session = Depends(get_db)):
    actualite = db.query(Actualites).filter(Actualites.id_actualite == actualite_id).first()
    if not actualite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actualité non trouvée"
        )

    db.delete(actualite)
    db.commit()
    return {"message": "Actualité supprimée avec succès"}