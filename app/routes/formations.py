from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Formations
from app.schemas import FormationCreate, FormationResponse

router = APIRouter()


@router.post("/", response_model=FormationResponse)
def create_formation(formation: FormationCreate, db: Session = Depends(get_db)):
    db_formation = Formations(**formation.dict())
    db.add(db_formation)
    db.commit()
    db.refresh(db_formation)
    return db_formation


@router.get("/", response_model=List[FormationResponse])
def get_formations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    formations = db.query(Formations).offset(skip).limit(limit).all()
    return formations


@router.get("/{formation_id}", response_model=FormationResponse)
def get_formation(formation_id: int, db: Session = Depends(get_db)):
    formation = db.query(Formations).filter(Formations.id_formation == formation_id).first()
    if not formation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Formation non trouvée"
        )
    return formation


@router.put("/{formation_id}", response_model=FormationResponse)
def update_formation(formation_id: int, formation: FormationCreate, db: Session = Depends(get_db)):
    db_formation = db.query(Formations).filter(Formations.id_formation == formation_id).first()
    if not db_formation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Formation non trouvée"
        )

    for key, value in formation.dict().items():
        setattr(db_formation, key, value)

    db.commit()
    db.refresh(db_formation)
    return db_formation


@router.delete("/{formation_id}")
def delete_formation(formation_id: int, db: Session = Depends(get_db)):
    formation = db.query(Formations).filter(Formations.id_formation == formation_id).first()
    if not formation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Formation non trouvée"
        )

    db.delete(formation)
    db.commit()
    return {"message": "Formation supprimée avec succès"}