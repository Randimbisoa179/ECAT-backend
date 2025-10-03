from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base


class Admin(Base):
    __tablename__ = "admin"

    id_admin = Column(Integer, primary_key=True, index=True)
    nom = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)


class Formations(Base):
    __tablename__ = "formations"

    id_formation = Column(Integer, primary_key=True, index=True)
    titre = Column(String(100), nullable=False)
    description = Column(Text)
    programme = Column(Text)
    image = Column(String(255))
    date_inscription = Column(TIMESTAMP, server_default=func.now())


class Actualites(Base):
    __tablename__ = "actualites"

    id_actualite = Column(Integer, primary_key=True, index=True)
    titre = Column(String(100), nullable=False)
    contenu = Column(Text)
    image = Column(String(255))
    date_publication = Column(TIMESTAMP, server_default=func.now())