#!/usr/bin/env python3
"""
Script de test pour la configuration SMTP avec domaine privé
"""

from app import app, mail
from flask_mail import Message


def test_smtp_prive():
    """Test de la configuration SMTP avec egpouli@epiphane-gedeon.com"""

    print("🔧 Test Configuration SMTP Domaine Privé")
    print("=" * 50)

    with app.app_context():
        # Afficher la configuration actuelle
        print("📋 Configuration SMTP actuelle :")
        print(f"   Serveur : {app.config['MAIL_SERVER']}")
        print(f"   Port    : {app.config['MAIL_PORT']}")
        print(f"   TLS     : {app.config['MAIL_USE_TLS']}")
        print(f"   User    : {app.config['MAIL_USERNAME']}")
        print(f"   Sender  : {app.config['MAIL_DEFAULT_SENDER']}")

        print("\n🧪 Test d'envoi d'email...")

        try:
            # Créer un email de test
            msg = Message(
                subject="[TEST] Configuration SMTP LACS",
                recipients=["egpouli@gmail.com"],  # Email de fallback pour test
                body="""
Ceci est un email de test pour vérifier la configuration SMTP.

Configuration testée :
- Serveur SMTP : {server}
- Port : {port}
- Expéditeur : {sender}

Si vous recevez cet email, la configuration fonctionne ! ✅

---
Email envoyé automatiquement par le système LACS
                """.format(
                    server=app.config["MAIL_SERVER"],
                    port=app.config["MAIL_PORT"],
                    sender=app.config["MAIL_DEFAULT_SENDER"],
                ),
                sender=app.config["MAIL_DEFAULT_SENDER"],
            )

            # Tentative d'envoi
            mail.send(msg)
            print("✅ Email de test envoyé avec succès !")
            print("📧 Vérifiez votre boîte mail : egpouli@gmail.com")

        except Exception as e:
            print(f"❌ Erreur lors de l'envoi : {e}")
            print("\n🔧 Solutions possibles :")
            print("1. Vérifiez les paramètres SMTP auprès de votre hébergeur")
            print("2. Testez différents ports (587, 465, 25)")
            print("3. Vérifiez le username/password de l'email")
            print("4. Consultez SMTP_CONFIG_PRIVE.md pour plus d'aide")

            return False

    return True


def afficher_aide_config():
    """Affiche l'aide pour configurer le SMTP"""

    print("\n" + "=" * 50)
    print("🆘 AIDE CONFIGURATION SMTP")
    print("=" * 50)

    print("\n📞 Qui contacter pour les paramètres SMTP :")
    print("   • Support de votre hébergeur web")
    print("   • Administrateur de epiphane-gedeon.com")
    print("   • Service client de votre registrar de domaine")

    print("\n📋 Informations à demander :")
    print("   • Serveur SMTP sortant")
    print("   • Port SMTP (587, 465, ou 25)")
    print("   • Type de sécurité (STARTTLS ou SSL)")
    print("   • Authentification requise (oui/non)")

    print("\n⚙️ Paramètres à tester :")
    print("   • mail.epiphane-gedeon.com:587 (STARTTLS)")
    print("   • mail.epiphane-gedeon.com:465 (SSL)")
    print("   • smtp.epiphane-gedeon.com:587")

    print("\n📖 Documentation complète :")
    print("   • Consultez SMTP_CONFIG_PRIVE.md")
    print("   • Exemples pour différents hébergeurs inclus")


if __name__ == "__main__":
    success = test_smtp_prive()
    if not success:
        afficher_aide_config()
