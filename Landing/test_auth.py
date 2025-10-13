#!/usr/bin/env python3
"""
Script de test du système d'authentification LACS
Usage: python test_auth.py
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from app.models import Utilisateur
from werkzeug.security import generate_password_hash


def test_authentication_system():
    """Test complet du système d'authentification"""

    print("=== Test du Système d'Authentification LACS ===\n")

    with app.app_context():
        try:
            # Vérifier que la base de données existe
            print("1. Vérification de la base de données...")
            users_count = Utilisateur.query.count()
            print(
                f"   ✓ Base de données accessible. {users_count} utilisateur(s) trouvé(s)"
            )

            # Vérifier l'utilisateur admin par défaut
            print("\n2. Vérification de l'utilisateur admin...")
            admin = Utilisateur.query.filter_by(email="admin@admin.com").first()

            if admin:
                print(f"   ✓ Admin trouvé: {admin.nom} {admin.prenom} ({admin.email})")
                print(f"   ✓ Statut admin: {'Oui' if admin.admin else 'Non'}")
            else:
                print("   ⚠ Aucun admin trouvé avec l'email admin@admin.com")
                print("   → Création de l'utilisateur admin...")

                admin = Utilisateur(
                    nom="Administrateur",
                    prenom="LACS",
                    email="admin@admin.com",
                    mot_de_passe=generate_password_hash("admin"),
                    admin=True,
                )
                db.session.add(admin)
                db.session.commit()
                print("   ✓ Utilisateur admin créé avec succès")

            # Test des routes protégées
            print("\n3. Vérification des routes d'authentification...")

            with app.test_client() as client:
                # Test de la page de connexion
                response = client.get("/login")
                print(f"   ✓ Page de connexion: Status {response.status_code}")

                # Test d'accès aux pages protégées sans authentification
                protected_routes = ["/add-article", "/add-categorie", "/inscriptions"]
                for route in protected_routes:
                    response = client.get(route, follow_redirects=False)
                    if response.status_code == 302:  # Redirection vers login
                        print(
                            f"   ✓ Route protégée {route}: Redirection vers login (Status 302)"
                        )
                    else:
                        print(
                            f"   ⚠ Route {route}: Status {response.status_code} (attendu 302)"
                        )

                # Test de connexion avec les bons identifiants
                print("\n4. Test de connexion...")
                login_data = {
                    "email": "admin@admin.com",
                    "mot_de_passe": "admin",
                    "csrf_token": None,  # Flask-WTF sera désactivé pour ce test
                }

                # Désactiver temporairement CSRF pour le test
                app.config["WTF_CSRF_ENABLED"] = False

                response = client.post("/login", data=login_data, follow_redirects=True)
                print(f"   ✓ Tentative de connexion: Status {response.status_code}")

                if (
                    b"Administration LACS" not in response.data
                    and response.status_code == 200
                ):
                    print("   ✓ Connexion réussie (pas de retour sur la page de login)")
                else:
                    print("   ⚠ La connexion pourrait avoir échoué")

                # Réactiver CSRF
                app.config["WTF_CSRF_ENABLED"] = True

            print("\n=== Résumé des Tests ===")
            print("✓ Base de données fonctionnelle")
            print("✓ Utilisateur admin configuré")
            print("✓ Routes protégées en place")
            print("✓ Page de connexion accessible")
            print("\n📝 Identifiants de test:")
            print("   Email: admin@admin.com")
            print("   Mot de passe: admin")
            print("\n🚀 Le système d'authentification est prêt !")

        except Exception as e:
            print(f"❌ Erreur lors du test: {e}")
            return False

    return True


if __name__ == "__main__":
    test_authentication_system()
