# Configuration des emails pour LACS
# Vous pouvez modifier ces paramètres selon vos besoins

# Configuration SMTP
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USE_TLS = True

# Remplacez ces valeurs par vos vraies informations
MAIL_USERNAME = "your-email@gmail.com"  # Email d'envoi
MAIL_PASSWORD = "your-app-password"  # Mot de passe d'application Gmail

# Emails de destination
PRIMARY_EMAIL = "egpouli@gmail.com"  # Email principal
FALLBACK_EMAIL = "egpouli@gmail.com"  # Email de secours

# Configuration de l'expéditeur
MAIL_DEFAULT_SENDER = "LACS Contact <noreply@lacs.tg>"

# Instructions pour configurer Gmail :
# 1. Activez l'authentification à 2 facteurs sur votre compte Gmail
# 2. Générez un "mot de passe d'application" dans les paramètres de sécurité
# 3. Utilisez ce mot de passe d'application dans MAIL_PASSWORD
# 4. Remplacez MAIL_USERNAME par votre adresse Gmail

print("📧 Configuration email chargée")
