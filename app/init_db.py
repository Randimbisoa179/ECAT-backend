from app.database import engine, Base, SessionLocal
from app.models import Admin, Formations, Actualites
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def init_database():
    # Créer toutes les tables
    Base.metadata.create_all(bind=engine)

    # Vérifier si un admin existe déjà
    db = SessionLocal()
    try:
        existing_admin = db.query(Admin).first()
        if not existing_admin:
            # Créer un admin par défaut
            default_admin = Admin(
                nom="Admin ECAT",
                email="admin@ecat-taratra.mg",
                password=pwd_context.hash("admin123")
            )
            db.add(default_admin)
            db.commit()
            print("✅ Base de données initialisée avec l'admin par défaut")
        else:
            print("✅ Base de données déjà initialisée")
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    init_database()