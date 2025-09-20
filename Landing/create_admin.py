#!/usr/bin/env python3
"""
Script pour créer un utilisateur administrateur
"""

from app import app, db
from app.models import Utilisateur
from werkzeug.security import generate_password_hash
import datetime


def create_admin_user():
    """
    Crée un utilisateur administrateur avec les identifiants par défaut
    """
    with app.app_context():
        try:
            # Vérifier si l'admin existe déjà
            existing_admin = Utilisateur.query.filter_by(
                email="admin@admin.com"
            ).first()

            if existing_admin:
                print("❌ Un utilisateur admin existe déjà avec cet email.")
                print(f"   ID: {existing_admin.id}")
                print(f"   Nom: {existing_admin.nom}")
                print(f"   Email: {existing_admin.email}")
                print(f"   Admin: {existing_admin.admin}")
                return False

            # Créer le nouvel utilisateur admin
            admin_user = Utilisateur(
                nom="Admin",
                prenom="Administrateur",
                numero_telephone="0000000000",  # Numéro par défaut
                email="admin@admin.com",
                mot_de_passe=generate_password_hash("admin"),
                admin=True,
                created_at=datetime.datetime.today().date(),
            )

            # Ajouter à la base de données
            db.session.add(admin_user)
            db.session.commit()

            print("✅ Utilisateur administrateur créé avec succès !")
            print(f"   Email: admin@admin.com")
            print(f"   Mot de passe: admin")
            print(f"   ID: {admin_user.id}")

            return True

        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur lors de la création de l'admin: {e}")
            return False


def reset_admin_password():
    """
    Remet à zéro le mot de passe de l'admin
    """
    with app.app_context():
        try:
            admin_user = Utilisateur.query.filter_by(email="admin@admin.com").first()

            if not admin_user:
                print("❌ Aucun utilisateur admin trouvé avec cet email.")
                return False

            # Réinitialiser le mot de passe
            admin_user.mot_de_passe = generate_password_hash("admin")
            admin_user.admin = True  # S'assurer qu'il est bien admin

            db.session.commit()

            print("✅ Mot de passe admin réinitialisé !")
            print(f"   Email: admin@admin.com")
            print(f"   Nouveau mot de passe: admin")

            return True

        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur lors de la réinitialisation: {e}")
            return False


def list_admin_users():
    """
    Liste tous les utilisateurs administrateurs
    """
    with app.app_context():
        try:
            admins = Utilisateur.query.filter_by(admin=True).all()

            if not admins:
                print("ℹ️ Aucun utilisateur administrateur trouvé.")
                return

            print(f"📋 Utilisateurs administrateurs ({len(admins)}):")
            print("-" * 50)

            for admin in admins:
                print(f"ID: {admin.id}")
                print(f"Nom: {admin.prenom} {admin.nom}")
                print(f"Email: {admin.email}")
                print(f"Téléphone: {admin.numero_telephone}")
                print(f"Créé le: {admin.created_at}")
                print("-" * 30)

        except Exception as e:
            print(f"❌ Erreur lors de la liste: {e}")


def delete_admin_user():
    """
    Supprime l'utilisateur admin par défaut (avec confirmation)
    """
    with app.app_context():
        try:
            admin_user = Utilisateur.query.filter_by(email="admin@admin.com").first()

            if not admin_user:
                print("❌ Aucun utilisateur admin trouvé avec cet email.")
                return False

            # Demander confirmation
            confirmation = input(
                f"⚠️ Êtes-vous sûr de vouloir supprimer l'admin '{admin_user.nom}' ? (oui/non): "
            )

            if confirmation.lower() in ["oui", "o", "yes", "y"]:
                db.session.delete(admin_user)
                db.session.commit()
                print("✅ Utilisateur admin supprimé avec succès.")
                return True
            else:
                print("❌ Suppression annulée.")
                return False

        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur lors de la suppression: {e}")
            return False


if __name__ == "__main__":
    print("=== Gestionnaire d'utilisateur administrateur ===\n")

    while True:
        print("Choisissez une action:")
        print("1. Créer un utilisateur admin")
        print("2. Réinitialiser le mot de passe admin")
        print("3. Lister les utilisateurs admin")
        print("4. Supprimer l'utilisateur admin")
        print("5. Quitter")

        choice = input("\nVotre choix (1-5): ").strip()

        if choice == "1":
            create_admin_user()
        elif choice == "2":
            reset_admin_password()
        elif choice == "3":
            list_admin_users()
        elif choice == "4":
            delete_admin_user()
        elif choice == "5":
            print("Au revoir !")
            break
        else:
            print("❌ Choix invalide. Veuillez choisir entre 1 et 5.")

        print("\n" + "=" * 50 + "\n")
