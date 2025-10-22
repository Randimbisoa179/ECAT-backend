from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import ContactMessage
from app.schemas import ContactMessageCreate

router = APIRouter(prefix="/api/contact-messages", tags=["Messages de Contact"])

@router.post("/")
async def create_contact_message(contact_message: ContactMessageCreate, db: Session = Depends(get_db)):
    db_contact_message = ContactMessage(**contact_message.dict())
    db.add(db_contact_message)
    db.commit()
    db.refresh(db_contact_message)
    return db_contact_message

@router.get("/")
async def get_contact_messages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contact_messages = db.query(ContactMessage).offset(skip).limit(limit).all()
    return contact_messages

@router.get("/{message_id}")
async def get_contact_message(message_id: int, db: Session = Depends(get_db)):
    contact_message = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()
    if not contact_message:
        raise HTTPException(status_code=404, detail="Message non trouvé")
    return contact_message

@router.put("/{message_id}")
async def update_contact_message(message_id: int, contact_message: ContactMessageCreate, db: Session = Depends(get_db)):
    db_contact_message = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()
    if not db_contact_message:
        raise HTTPException(status_code=404, detail="Message non trouvé")

    for key, value in contact_message.dict().items():
        setattr(db_contact_message, key, value)

    db.commit()
    db.refresh(db_contact_message)
    return db_contact_message

@router.delete("/{message_id}")
async def delete_contact_message(message_id: int, db: Session = Depends(get_db)):
    contact_message = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()
    if not contact_message:
        raise HTTPException(status_code=404, detail="Message non trouvé")

    db.delete(contact_message)
    db.commit()
    return {"message": "Message supprimé avec succès"}