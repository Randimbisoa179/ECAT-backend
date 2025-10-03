import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Chargement robuste du .env
def load_environment():
    """Charger les variables d'environnement depuis .env"""
    try:
        from dotenv import load_dotenv
        # Essayer plusieurs emplacements possibles
        paths = [
            os.path.join(os.path.dirname(__file__), '..', '.env'),  # ../.env depuis app/
            '.env',  # Répertoire courant
            '/home/randimbisoa/Bureau/stage/back/.env'  # Chemin absolu
        ]

        for path in paths:
            if os.path.exists(path):
                load_dotenv(path)
                print(f"✅ Fichier .env chargé: {path}")
                return True

        print("⚠️  Aucun fichier .env trouvé")
        return False

    except ImportError:
        print("⚠️  python-dotenv non installé")
        return False


# Charger l'environnement
load_environment()

# Récupérer DATABASE_URL avec valeur par défaut
DATABASE_URL = os.getenv("postgresql://neondb_owner:npg_oxpDnBG9mc8T@ep-withered-cake-adjaqyv0-pooler.c-2.us-east-1.aws.neon.tech/db_univ?sslmode=require&channel_binding=require")

if not DATABASE_URL:
    DATABASE_URL = "postgresql://neondb_owner:npg_oxpDnBG9mc8T@ep-withered-cake-adjaqyv0-pooler.c-2.us-east-1.aws.neon.tech/db_univ?sslmode=require&channel_binding=require"
    print("🔧 Utilisation de la base de données par défaut")

print(f"🔗 Connexion à: {DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else DATABASE_URL}")

# Configuration de la base de données
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()