from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# Schemas pour Admin
class AdminBase(BaseModel):
    nom: str
    email: EmailStr


class AdminCreate(AdminBase):
    password: str


class AdminResponse(AdminBase):
    id_admin: int

    class Config:
        from_attributes = True


# Schemas pour Formations
class FormationBase(BaseModel):
    titre: str
    description: Optional[str] = None
    programme: Optional[str] = None
    image: Optional[str] = None


class FormationCreate(FormationBase):
    pass


class FormationResponse(FormationBase):
    id_formation: int
    date_inscription: datetime

    class Config:
        from_attributes = True


# Schemas pour Actualités
class ActualiteBase(BaseModel):
    titre: str
    contenu: Optional[str] = None
    image: Optional[str] = None


class ActualiteCreate(ActualiteBase):
    pass


class ActualiteResponse(ActualiteBase):
    id_actualite: int
    date_publication: datetime

    class Config:
        from_attributes = True