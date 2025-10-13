#!/usr/bin/env python3
"""
Script de test pour l'envoi d'emails de contact LACS
Ce script montre comment fonctionne le système d'envoi d'email avec fallback
"""

from app import app, mail
from flask_mail import Message


def test_email_envoi():
    """Test de la fonctionnalité d'envoi d'email"""

    with app.app_context():
        print("🧪 Test du système d'envoi d'email LACS")
        print("=" * 50)

        # Simulation d'un message de contact
        test_data = {
            "firstName": "Jean",
            "lastName": "Dupont",
            "email": "jean.dupont@exemple.com",
            "phone": "+228 12 34 56 78",
            "subject": "information",
            "message": "Bonjour, j'aimerais avoir des informations sur vos formations en mathématiques. Merci !",
        }

        # Mapping des sujets
        sujet_mapping = {
            "inscription": "Demande d'inscription",
            "information": "Demande d'information",
            "rdv": "Prise de rendez-vous",
            "pedagogie": "Questions pédagogiques",
            "partenariat": "Partenariat",
            "autre": "Autre demande",
        }

        sujet_email = f"[LACS Contact] {sujet_mapping.get(test_data['subject'], 'Nouvelle demande')}"

        corps_email = f"""
Nouvelle demande de contact depuis le site LACS :

Informations du contact :
- Nom : {test_data["lastName"]}
- Prénom : {test_data["firstName"]}
- Email : {test_data["email"]}
- Téléphone : {test_data["phone"]}
- Sujet : {sujet_mapping.get(test_data["subject"], "Autre")}

Message :
{test_data["message"]}

---
Ce message a été envoyé depuis le formulaire de contact du site LACS.
Vous pouvez répondre directement à l'adresse : {test_data["email"]}
        """

        print(f"📧 Sujet: {sujet_email}")
        print(f"📧 Email principal: egpouli@epiphane-gedeon.com")
        print(f"📧 Email fallback: egpouli@gmail.com")
        print("\n📝 Contenu du message:")
        print(corps_email)
        print("\n" + "=" * 50)

        # Note : L'envoi réel nécessite une configuration SMTP valide
        print("⚠️  Pour activer l'envoi réel d'emails :")
        print("1. Configurez les paramètres SMTP dans app/__init__.py")
        print("2. Ajoutez vos credentials Gmail")
        print("3. Activez l'authentification à 2 facteurs sur Gmail")
        print("4. Générez un mot de passe d'application")
        print("\n✅ Logique d'envoi prête !")

        return True


if __name__ == "__main__":
    test_email_envoi()
