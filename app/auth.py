from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from pydantic import BaseModel

# Importations des composants locaux
from app.database import get_db
from app.models import Admin
from app.schemas import LoginResponse

# === Configuration ===
SECRET_KEY = "UzevKfUdK2muiPIvVgnQRn3JXejrgaA2bHlPOSnXX74"  # ⚠️ REMPLACEZ ceci par une clé sécurisée !
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 heures


# 🚨 Modèle Pydantic pour lire le corps JSON de la requête de login
class LoginCredentials(BaseModel):
    email: str
    password: str


# Initialisation
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()


# === Fonctions utilitaires ===
def get_password_hash(password: str) -> str:
    """Génère le hachage Bcrypt pour un mot de passe clair."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie un mot de passe clair par rapport à un hachage."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crée un jeton JWT avec une expiration."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_admin(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
) -> Admin:
    """Décode le jeton JWT et récupère l'objet Admin pour les routes sécurisées."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        admin_id_str = payload.get("sub")
        # Récupère le rôle du token (pour vérification des permissions si nécessaire)
        role = payload.get("role")
        if not admin_id_str:
            raise credentials_exception
        admin_id = int(admin_id_str)
    except (JWTError, ValueError):
        raise credentials_exception

    admin = db.query(Admin).filter(Admin.id_admin == admin_id).first()
    if not admin:
        raise credentials_exception
    return admin


def authenticate_admin(db: Session, email: str, password: str):
    """Authentifie un administrateur par email et mot de passe."""
    admin = db.query(Admin).filter(Admin.email == email).first()
    if not admin:
        return False
    if not verify_password(password, admin.password_hash):
        return False
    return admin


# === Route Login ===
@router.post("/login", response_model=LoginResponse)
def login(credentials: LoginCredentials, db: Session = Depends(get_db)):
    """Authentifie un administrateur et retourne un jeton d'accès et les informations de l'admin."""
    email = credentials.email
    password = credentials.password

    admin = db.query(Admin).filter(Admin.email == email).first()

    # Logique d'autorisation
    try:
        # Lève HTTPException si l'admin n'existe pas ou si le mot de passe ne correspond pas.
        if not admin or not verify_password(password, admin.password_hash):
            # Utilisez le même message pour la sécurité (ne pas divulguer si l'email existe ou non)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou mot de passe incorrect"
            )

    except UnknownHashError:
        # Attrape l'erreur si le password_hash dans la DB est mal formaté
        print(f"Erreur de données: Hachage non identifié pour l'administrateur {email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )

    # Si la vérification réussit, inclut le rôle dans le token
    token = create_access_token(data={
        "sub": str(admin.id_admin),
        "role": admin.role
    })

    # Renvoie les données complètes attendues par le frontend (LoginResponse)
    return {
        "access_token": token,
        "token_type": "bearer",
        "admin_id": admin.id_admin,
        "nom": admin.nom,
        "email": admin.email,
        "role": admin.role  # ✅ Le rôle est inclus dans la réponse JSON
    }