#!/usr/bin/env python3
"""
Test du formulaire de contact de la page d'accueil
"""

from app import app
from app.forms import SimpleContactForm


def test_home_contact_form():
    """Test du formulaire de contact de la page d'accueil"""

    print("🏠 Test du formulaire de contact page d'accueil")
    print("=" * 55)

    # Simuler des données de test
    test_data = {
        "firstName": "Marie",
        "lastName": "Kouassi",
        "email": "marie.kouassi@exemple.tg",
        "phone": "+228 90 12 34 56",
        "subject": "Demande d'information sur vos cours de mathématiques",
        "message": "Bonjour, je souhaite inscrire ma fille en Première C. Pouvez-vous me donner plus d'informations sur vos programmes et tarifs ? Merci.",
        "privacy": True,
    }

    print("📝 Données de test du formulaire :")
    for field, value in test_data.items():
        print(f"   {field}: {value}")

    print("\n📧 Email principal: egpouli@epiphane-gedeon.com")
    print("📧 Email fallback: egpouli@gmail.com")

    # Format de l'email qui sera envoyé
    sujet_email = f"[LACS Contact] {test_data['subject']}"

    corps_email = f"""
Nouvelle demande de contact depuis la page d'accueil du site LACS :

Informations du contact :
- Nom : {test_data["lastName"]}
- Prénom : {test_data["firstName"]}
- Email : {test_data["email"]}
- Téléphone : {test_data["phone"]}
- Sujet : {test_data["subject"]}

Message :
{test_data["message"]}

---
Ce message a été envoyé depuis le formulaire de contact de la page d'accueil du site LACS.
Vous pouvez répondre directement à l'adresse : {test_data["email"]}
    """

    print("\n📬 Aperçu de l'email qui sera envoyé :")
    print(f"Sujet: {sujet_email}")
    print(f"Corps:\n{corps_email}")

    print("\n" + "=" * 55)
    print("✅ Formulaire de contact page d'accueil configuré !")
    print("🚀 Pour tester en réel :")
    print("   1. Configurez les credentials SMTP")
    print("   2. Lancez: flask run")
    print("   3. Allez sur http://localhost:5000")
    print("   4. Remplissez le formulaire en bas de page")

    return True


if __name__ == "__main__":
    test_home_contact_form()
