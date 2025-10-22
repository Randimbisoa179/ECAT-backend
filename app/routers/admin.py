from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Admin
from app.schemas import AdminCreate, AdminResponse, AdminUpdate
from app.auth import get_password_hash, get_current_admin

router = APIRouter(prefix="/api/admins", tags=["Administrateurs"])


@router.get("/me", response_model=AdminResponse)
async def get_current_admin_endpoint(current_admin: Admin = Depends(get_current_admin)):
    """
    Récupérer les informations de l'administrateur connecté (nécessite un token Bearer)
    """
    return current_admin


@router.post("/", response_model=AdminResponse, status_code=status.HTTP_201_CREATED)
async def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    existing_admin = db.query(Admin).filter(Admin.email == admin.email).first()
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un administrateur avec cet email existe déjà"
        )

    hashed_password = get_password_hash(admin.password)

    db_admin = Admin(
        nom=admin.nom,
        email=admin.email,
        password_hash=hashed_password,
        role=admin.role
    )

    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


@router.get("/", response_model=List[AdminResponse])
async def get_admins(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_admin: Admin = Depends(get_current_admin)
):
    admins = db.query(Admin).offset(skip).limit(limit).all()
    return admins


@router.get("/{admin_id}", response_model=AdminResponse)
async def get_admin(admin_id: int, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.id_admin == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Administrateur non trouvé")
    return admin


@router.put("/{admin_id}", response_model=AdminResponse)
async def update_admin(
        admin_id: int,
        admin_update: AdminUpdate,
        db: Session = Depends(get_db),
        current_admin: Admin = Depends(get_current_admin)
):
    db_admin = db.query(Admin).filter(Admin.id_admin == admin_id).first()
    if not db_admin:
        raise HTTPException(status_code=404, detail="Administrateur non trouvé")

    if admin_update.email:
        existing_admin = db.query(Admin).filter(
            Admin.email == admin_update.email,
            Admin.id_admin != admin_id
        ).first()
        if existing_admin:
            raise HTTPException(
                status_code=400,
                detail="Un administrateur avec cet email existe déjà"
            )

    update_data = admin_update.dict(exclude_unset=True)

    if 'password' in update_data and update_data['password']:
        update_data['password_hash'] = get_password_hash(update_data['password'])
        del update_data['password']

    for key, value in update_data.items():
        setattr(db_admin, key, value)

    db.commit()
    db.refresh(db_admin)
    return db_admin


@router.delete("/{admin_id}")
async def delete_admin(
        admin_id: int,
        db: Session = Depends(get_db),
        current_admin: Admin = Depends(get_current_admin)
):
    admin = db.query(Admin).filter(Admin.id_admin == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Administrateur non trouvé")

    total_admins = db.query(Admin).count()
    if total_admins <= 1:
        raise HTTPException(
            status_code=400,
            detail="Impossible de supprimer le dernier administrateur"
        )

    db.delete(admin)
    db.commit()
    return {"message": "Administrateur supprimé avec succès"}