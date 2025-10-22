from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import ContactInfo
from app.schemas import ContactInfoCreate

router = APIRouter(prefix="/api/contact-info", tags=["Informations de Contact"])

@router.post("/")
async def create_contact_info(contact_info: ContactInfoCreate, db: Session = Depends(get_db)):
    db_contact_info = ContactInfo(**contact_info.dict())
    db.add(db_contact_info)
    db.commit()
    db.refresh(db_contact_info)
    return db_contact_info

@router.get("/")
async def get_contact_infos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contact_infos = db.query(ContactInfo).offset(skip).limit(limit).all()
    return contact_infos

@router.get("/{info_id}")
async def get_contact_info(info_id: int, db: Session = Depends(get_db)):
    contact_info = db.query(ContactInfo).filter(ContactInfo.id == info_id).first()
    if not contact_info:
        raise HTTPException(status_code=404, detail="Info contact non trouvée")
    return contact_info

@router.put("/{info_id}")
async def update_contact_info(info_id: int, contact_info: ContactInfoCreate, db: Session = Depends(get_db)):
    db_contact_info = db.query(ContactInfo).filter(ContactInfo.id == info_id).first()
    if not db_contact_info:
        raise HTTPException(status_code=404, detail="Info contact non trouvée")

    for key, value in contact_info.dict().items():
        setattr(db_contact_info, key, value)

    db.commit()
    db.refresh(db_contact_info)
    return db_contact_info

@router.delete("/{info_id}")
async def delete_contact_info(info_id: int, db: Session = Depends(get_db)):
    contact_info = db.query(ContactInfo).filter(ContactInfo.id == info_id).first()
    if not contact_info:
        raise HTTPException(status_code=404, detail="Info contact non trouvée")

    db.delete(contact_info)
    db.commit()
    return {"message": "Info contact supprimée avec succès"}