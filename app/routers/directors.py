from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Director
from app.schemas import DirectorCreate

router = APIRouter(prefix="/api/directors", tags=["Directeurs"])

@router.post("/")
async def create_director(director: DirectorCreate, db: Session = Depends(get_db)):
    db_director = Director(**director.dict())
    db.add(db_director)
    db.commit()
    db.refresh(db_director)
    return db_director

@router.get("/")
async def get_directors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    directors = db.query(Director).offset(skip).limit(limit).all()
    return directors

@router.get("/{director_id}")
async def get_director(director_id: int, db: Session = Depends(get_db)):
    director = db.query(Director).filter(Director.id == director_id).first()
    if not director:
        raise HTTPException(status_code=404, detail="Directeur non trouvé")
    return director

@router.put("/{director_id}")
async def update_director(director_id: int, director: DirectorCreate, db: Session = Depends(get_db)):
    db_director = db.query(Director).filter(Director.id == director_id).first()
    if not db_director:
        raise HTTPException(status_code=404, detail="Directeur non trouvé")

    for key, value in director.dict().items():
        setattr(db_director, key, value)

    db.commit()
    db.refresh(db_director)
    return db_director

@router.delete("/{director_id}")
async def delete_director(director_id: int, db: Session = Depends(get_db)):
    director = db.query(Director).filter(Director.id == director_id).first()
    if not director:
        raise HTTPException(status_code=404, detail="Directeur non trouvé")

    db.delete(director)
    db.commit()
    return {"message": "Directeur supprimé avec succès"}