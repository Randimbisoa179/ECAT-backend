from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import AboutContent
from app.schemas import AboutContentCreate

router = APIRouter(prefix="/api/about-content", tags=["À Propos"])

@router.post("/")
async def create_about_content(about_content: AboutContentCreate, db: Session = Depends(get_db)):
    db_about_content = AboutContent(**about_content.dict())
    db.add(db_about_content)
    db.commit()
    db.refresh(db_about_content)
    return db_about_content

@router.get("/")
async def get_about_contents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    about_contents = db.query(AboutContent).offset(skip).limit(limit).all()
    return about_contents

@router.get("/{content_id}")
async def get_about_content(content_id: int, db: Session = Depends(get_db)):
    about_content = db.query(AboutContent).filter(AboutContent.id == content_id).first()
    if not about_content:
        raise HTTPException(status_code=404, detail="Contenu About non trouvé")
    return about_content

@router.put("/{content_id}")
async def update_about_content(content_id: int, about_content: AboutContentCreate, db: Session = Depends(get_db)):
    db_about_content = db.query(AboutContent).filter(AboutContent.id == content_id).first()
    if not db_about_content:
        raise HTTPException(status_code=404, detail="Contenu About non trouvé")

    for key, value in about_content.dict().items():
        setattr(db_about_content, key, value)

    db.commit()
    db.refresh(db_about_content)
    return db_about_content

@router.delete("/{content_id}")
async def delete_about_content(content_id: int, db: Session = Depends(get_db)):
    about_content = db.query(AboutContent).filter(AboutContent.id == content_id).first()
    if not about_content:
        raise HTTPException(status_code=404, detail="Contenu About non trouvé")

    db.delete(about_content)
    db.commit()
    return {"message": "Contenu About supprimé avec succès"}