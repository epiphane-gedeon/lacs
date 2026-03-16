from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupération des informations de connexion à la base de données
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")

# Construction de l'URL de la base de données
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Création de l'engine avec un pooling configuré
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
)

# Configuration de la session locale
SessionLocal = sessionmaker(engine, class_=Session, expire_on_commit=False)

# Base déclarative
Base = declarative_base()


# Gestion des sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"Erreur de base de données : {e}")
        raise
    finally:
        db.close()
