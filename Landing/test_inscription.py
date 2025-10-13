#!/usr/bin/env python3
"""
Script de test pour la logique d'inscription
"""

from app import app, db
from app.models import Utilisateur, Eleve, Parent, Inscription
import datetime


def test_matricule_generation():
    """Test de génération de matricule"""
    with app.app_context():
        # Simuler quelques élèves existants
        annee_courte = str(datetime.datetime.now().year)[-2:]

        # Vérifier la logique de génération
        from app.routes import generer_matricule

        try:
            matricule = generer_matricule()
            print(f"Matricule généré: {matricule}")

            # Vérifier le format
            parts = matricule.split("-")
            if len(parts) == 3 and parts[0] == "LACS" and parts[1] == annee_courte:
                print("✅ Format du matricule correct")

                # Vérifier la partie lettre-nombre
                lettre_numero = parts[2]
                if (
                    len(lettre_numero) == 4
                    and lettre_numero[0].isalpha()
                    and lettre_numero[1:].isdigit()
                ):
                    print("✅ Format lettre-nombre correct")
                else:
                    print("❌ Format lettre-nombre incorrect")
            else:
                print("❌ Format du matricule incorrect")

        except Exception as e:
            print(f"❌ Erreur lors de la génération: {e}")


def test_code_parent_generation():
    """Test de génération de code parent"""
    with app.app_context():
        from app.routes import generer_code_parent

        try:
            code = generer_code_parent()
            print(f"Code parent généré: {code}")

            # Vérifier le format PAR-YYYY-NNN
            parts = code.split("-")
            if (
                len(parts) == 3
                and parts[0] == "PAR"
                and parts[1].isdigit()
                and parts[2].isdigit()
            ):
                print("✅ Format du code parent correct")
            else:
                print("❌ Format du code parent incorrect")

        except Exception as e:
            print(f"❌ Erreur lors de la génération: {e}")


if __name__ == "__main__":
    print("=== Test de la logique d'inscription ===\n")

    print("1. Test de génération de matricule:")
    test_matricule_generation()

    print("\n2. Test de génération de code parent:")
    test_code_parent_generation()

    print("\n=== Fin des tests ===")
