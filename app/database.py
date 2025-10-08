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

        print("⚠️ Aucun fichier .env trouvé")
        return False

    except ImportError:
        print("⚠️ python-dotenv non installé")
        return False


# Charger l'environnement
load_environment()

# 🚨 CORRECTION MAJEURE ICI 🚨
# 1. Définir l'URL de connexion complète et la stocker.
# On retire les paramètres avancés (&channel_binding=require) qui peuvent causer le crash.
NEON_DB_URL = "postgresql://neondb_owner:npg_oxpDnBG9mc8T@ep-withered-cake-adjaqyv0-pooler.c-2.us-east-1.aws.neon.tech/db_univ"

# 2. Tenter de lire une variable nommée "DATABASE_URL" depuis l'environnement.
# Si elle n'est pas trouvée (si le .env est absent ou mal configuré), on utilise l'URL Neon par défaut.
DATABASE_URL = os.getenv("DATABASE_URL", NEON_DB_URL)


print(f"🔗 Connexion à: {DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else DATABASE_URL}")

# Configuration de la base de données
# 🚨 Ajout du paramètre 'connect_args' pour forcer le mode SSL, nécessaire pour Neon.
engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"} 
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

