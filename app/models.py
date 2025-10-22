# app/models.py - VERSION CORRIGÉE
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from app.database import Base

class Admin(Base):
    __tablename__ = "admin"
    
    id_admin = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(60), nullable=False)  # ✅ Indentation corrigée
    role = Column(String(50), default='admin', nullable=False)
    
class Formations(Base):
    __tablename__ = "formations"
    
    id_formation = Column(Integer, primary_key=True, index=True)
    titre = Column(String(255), nullable=False)
    description = Column(Text)
    programme = Column(Text)
    image = Column(String(500))
    date_inscription = Column(DateTime(timezone=True), server_default=func.now())

class Actualites(Base):
    __tablename__ = "actualites"
    
    id_actualite = Column(Integer, primary_key=True, index=True)
    titre = Column(String(255), nullable=False)
    contenu = Column(Text)
    image = Column(String(500))
    categorie = Column(String(255), nullable=False)
    date_publication = Column(DateTime(timezone=True), server_default=func.now())


class Director(Base):
    __tablename__ = "directors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    bio = Column(Text)
    email = Column(String(255))
    photo_url = Column(String(500))
    message = Column(Text)
    start_date = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class AboutContent(Base):
    __tablename__ = "about_content"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    mission = Column(Text)
    vision = Column(Text)
    history = Column(Text)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ContactInfo(Base):
    __tablename__ = "contact_info"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)
    address = Column(Text, nullable=False)
    map_url = Column(String(500))
    social_media = Column(Text)  # Stocké comme JSON string ou texte
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_read = Column(Boolean, default=False)

