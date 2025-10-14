from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from typing import Optional, List, Dict, Any

class Token(BaseModel):
    access_token: str
    token_type: str
    admin_id: int
    nom: str
    email: str

class TokenData(BaseModel):
    admin_id: Optional[int] = None

# Schemas pour Admin
class AdminBase(BaseModel):
    nom: str
    email: EmailStr
    
class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    admin_id: int
    nom: str
    email: str

class AdminCreate(AdminBase):
    password: str

class AdminUpdate(BaseModel):
    nom: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

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
    categorie: str


class ActualiteCreate(ActualiteBase):
    pass


class ActualiteResponse(ActualiteBase):
    id_actualite: int
    date_publication: datetime

    class Config:
        from_attributes = True


class DirectorBase(BaseModel):
    name: str
    title: str
    bio: Optional[str] = None
    email: Optional[EmailStr] = None
    photo_url: Optional[str] = None
    message: Optional[str] = None
    start_date: Optional[datetime] = None


class DirectorCreate(DirectorBase):
    pass


class DirectorUpdate(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    bio: Optional[str] = None
    email: Optional[EmailStr] = None
    photo_url: Optional[str] = None
    message: Optional[str] = None
    start_date: Optional[datetime] = None


class DirectorResponse(DirectorBase):
    id: int
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== ABOUT CONTENT SCHEMAS ====================

class AboutContentBase(BaseModel):
    title: str
    description: Optional[str] = None
    mission: Optional[str] = None
    vision: Optional[str] = None
    history: Optional[str] = None


class AboutContentCreate(AboutContentBase):
    pass


class AboutContentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    mission: Optional[str] = None
    vision: Optional[str] = None
    history: Optional[str] = None


class AboutContentResponse(AboutContentBase):
    id: int
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== CONTACT INFO SCHEMAS ====================

class ContactInfoBase(BaseModel):
    email: EmailStr
    phone: str
    address: str
    map_url: Optional[str] = None
    social_media: Optional[str] = None


class ContactInfoCreate(ContactInfoBase):
    pass


class ContactInfoUpdate(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    map_url: Optional[str] = None
    social_media: Optional[str] = None


class ContactInfoResponse(ContactInfoBase):
    id: int
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== CONTACT MESSAGE SCHEMAS ====================

class ContactMessageBase(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str


class ContactMessageCreate(ContactMessageBase):
    pass


class ContactMessageUpdate(BaseModel):
    is_read: Optional[bool] = None


class ContactMessageResponse(ContactMessageBase):
    id: int
    created_at: datetime
    is_read: bool

    class Config:
        from_attributes = True


# ==================== SCHEMAS POUR LES RÉPONSES DÉTAILLÉES ====================

class AboutPageResponse(BaseModel):
    about_content: AboutContentResponse
    directors: List[DirectorResponse]


class ContactPageResponse(BaseModel):
    contact_info: ContactInfoResponse
    recent_messages: List[ContactMessageResponse]


# ==================== SCHEMAS POUR LES STATISTIQUES ====================

class MessageStatsResponse(BaseModel):
    total_messages: int
    unread_messages: int
    read_messages: int


# ==================== SCHEMAS POUR LES RECHERCHES/FILTRES ====================

class MessageFilter(BaseModel):
    is_read: Optional[bool] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    email: Optional[EmailStr] = None


class DirectorFilter(BaseModel):
    title: Optional[str] = None