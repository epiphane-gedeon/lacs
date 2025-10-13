from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_url
from flask_mail import Mail
import locale
from datetime import datetime

app = Flask(__name__)

app.config["SECRET_KEY"] = "j-ITiFqDJMq2bqXLf3-DIg"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lacs.db"
app.secret_key = "secret key"

# Configuration pour l'envoi d'emails
# ✅ Serveur SMTP détecté : web56.lws-hosting.com (LWS Hosting)
app.config["MAIL_SERVER"] = "mail.epiphane-gedeon.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "contact@epiphane-gedeon.com"
app.config["MAIL_PASSWORD"] = "(cI;87ypCeQ.wEkI"  # ⚠️ À CONFIGURER
app.config["MAIL_DEFAULT_SENDER"] = "LACS Contact <contact@epiphane-gedeon.com>"

# Option 2: Gmail avec alias (si Option 1 ne marche pas)
# app.config["MAIL_SERVER"] = "smtp.gmail.com"
# app.config["MAIL_PORT"] = 587
# app.config["MAIL_USE_TLS"] = True
# app.config["MAIL_USERNAME"] = "serveurgak@gmail.com"
# app.config["MAIL_PASSWORD"] = "phdc twxj phhu kfyw"
# app.config["MAIL_DEFAULT_SENDER"] = "LACS Contact <egpouli@epiphane-gedeon.com>"

app.config["MAIL_DEBUG"] = True  # Pour déboguer les emails en développement

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    from app.models import Utilisateur

    return Utilisateur.query.get(int(user_id))


bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)


# Filtre personnalisé pour formater les dates en français
def format_date_fr(date_value, format_type="date"):
    if not date_value:
        return ""

    # Dictionnaire des mois en français
    mois_fr = {
        1: "janv",
        2: "fév",
        3: "mar",
        4: "avr",
        5: "mai",
        6: "juin",
        7: "juil",
        8: "août",
        9: "sep",
        10: "oct",
        11: "nov",
        12: "déc",
    }

    if isinstance(date_value, str):
        date_value = datetime.strptime(date_value, "%Y-%m-%d").date()

    jour = date_value.day
    mois = mois_fr[date_value.month]
    annee = date_value.year

    if format_type == "date":
        return f"{jour} {mois} {annee}"
    elif format_type == "court":
        return f"{jour} {mois[:3]}. {annee}"
    else:
        return f"{jour} {mois} {annee}"


# Enregistrer le filtre
app.jinja_env.filters["date_fr"] = format_date_fr

from app import routes
