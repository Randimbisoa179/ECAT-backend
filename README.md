## 🚀 ECAT Backend

Backend du projet ECAT, développé avec FastAPI et PostgreSQL, servant d’API pour la gestion des formations, des actualités et de l’administration.

## Table de matiéres
Aperçu

Fonctionnalités

Architecture du projet

Installation

Configuration

Démarrage du serveur

Endpoints principaux

Déploiement


## 📘 Aperçu
Ce projet constitue le backend de l’application ECAT.
Il fournit une API REST permettant à l’administrateur de gérer les formations et les actualités via des opérations CRUD (Create, Read, Update, Delete).

Le système d’administration est sécurisé par une authentification basée sur l’email et le mot de passe de l’administrateur.
## ⚙️ Fonctionnalités
🔐 Authentification admin (email statique défini dans le backend)

📚 Gestion des formations (ajout, modification, suppression, consultation)

📰 Gestion des actualités (CRUD complet)

🧾 Base de données PostgreSQL

🌐 API REST conforme à la documentation OpenAPI (Swagger / Redoc intégrée)

🧠 Validation automatique des données avec Pydantic

🚀 Serveur rapide grâce à Uvicorn
## 🗂️ Architecture du projet

```bash
ECAT-backend/
├── app/
│   ├── main.py              # Point d’entrée de l’application FastAPI
│   ├── models/              # Modèles SQLAlchemy
│   │   ├── admin.py
│   │   ├── formation.py
│   │   └── actualite.py
│   │── routers/ 
│   ├── schemas/             # Schémas Pydantic (validation / sérialisation)
│   ├── database.py          # Connexion à PostgreSQL
│   ├── utils/               # Fonctions utilitaires
│   └── __init__.py
├── requirements.txt         # Dépendances du projet
├── .env                     # Variables d’environnement
├── README.md
└── vercel.json / Procfile   # (si déploiement)
```
## 🛠️ Installation
Prérequis

Python 3.10 ou supérieur

PostgreSQL installé et en cours d’exécution

pip et virtualenv

Étapes
```bash
# Cloner le projet
git clone https://github.com/Randimbisoa179/ECAT-backend.git
cd ECAT-backend

# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # macOS / Linux
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt
```

## ⚙️ Configuration
Créer un fichier .env à la racine avec le contenu suivant :
```bash
# Variables d’environnement

DATABASE_URL=postgresql://username:password@localhost:5432/db_univ
ADMIN_EMAIL=admin@ecat.com
ADMIN_PASSWORD=motdepassefort
SECRET_KEY=secret_key_unique
DEBUG=True

```
💡 Remarque :
L’adresse email de l’admin est statique et définie dans le backend pour empêcher l’accès non autorisé.
## 🏃‍♂️ Démarrage du serveur
Lancer le serveur en local :
```bash
uvicorn app.main:app --reload
```
Par défaut, l’API sera disponible sur :
👉 http://127.0.0.1:8000

La documentation automatique :

Swagger UI : http://127.0.0.1:8000/docs

Redoc : http://127.0.0.1:8000/redoc
## 🔗 Endpoints principaux
| Méthode | Endpoint | Description |
|----------|-----------|-------------|
| **POST** | `/api/admin/login` | Connexion de l’administrateur |
| **GET** | `/api/formations` | Liste des formations |
| **POST** | `/api/formations` | Ajouter une formation |
| **PUT** | `/api/formations/{id}` | Modifier une formation |
| **DELETE** | `/api/formations/{id}` | Supprimer une formation |
| **GET** | `/api/actualites` | Liste des actualités |
| **POST** | `/api/actualites` | Ajouter une actualité |
| **PUT** | `/api/actualites/{id}` | Modifier une actualité |
| **DELETE** | `/api/actualites/{id}` | Supprimer une actualité |

## 🚀 Déploiement
Sur Vercel / Render / Railway

Ajouter les variables d’environnement dans le tableau de bord du service.

S’assurer que le fichier vercel.json ou Procfile est configuré.

Lancer le déploiement automatique à partir du dépôt GitHub.

Exemple Procfile :
```bash
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT

```
