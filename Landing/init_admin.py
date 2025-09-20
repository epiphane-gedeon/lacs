#!/usr/bin/env python3
"""
Script rapide pour créer un admin
Usage: python init_admin.py
"""

from app import app
from app.utils import create_admin

if __name__ == "__main__":
    print("=== Création de l'utilisateur administrateur ===")

    with app.app_context():
        success = create_admin()

        if success:
            print("\n🎉 Vous pouvez maintenant vous connecter avec:")
            print("   Email: admin@admin.com")
            print("   Mot de passe: admin")
        else:
            print("\n❌ La création a échoué.")

    print("\n=== Fin du script ===")
