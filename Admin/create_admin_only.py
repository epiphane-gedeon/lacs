#!/usr/bin/env python3
"""
Script pour créer un utilisateur administrateur dans la base de données
"""

import sys
import os
import uuid
from datetime import datetime

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine
from app.models import Base, Utilisateur, Administrateur
from app.auth import hash_password

# Créer les tables si elles n'existent pas
Base.metadata.create_all(bind=engine)


def create_admin():
    """Créer l'administrateur de test"""
    db = SessionLocal()

    try:
        # Vérifier si l'admin existe déjà
        admin_exists = (
            db.query(Utilisateur).filter(Utilisateur.email == "admin@lacs.com").first()
        )

        if admin_exists:
            print("✅ L'administrateur existe déjà!")
            print(f"   Email: admin@lacs.com")
            print(f"   Mot de passe: admin123")
            return

        # Créer l'utilisateur admin
        admin_user = Utilisateur(
            id=uuid.uuid4(),
            email="admin@lacs.com",
            name="Administrateur",
            firstname="Admin",
            password=hash_password("admin123"),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        db.add(admin_user)
        db.flush()

        # Créer le profil administrateur lié
        admin_profile = Administrateur(id=uuid.uuid4(), user_id=admin_user.id)

        db.add(admin_profile)
        db.commit()

        print("✅ Administrateur créé avec succès!")
        print(f"   Email: admin@lacs.com")
        print(f"   Mot de passe: admin123")

    except Exception as e:
        db.rollback()
        print(f"❌ Erreur: {e}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
