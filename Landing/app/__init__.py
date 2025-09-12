from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_url
import locale
from datetime import datetime

app = Flask(__name__)

app.config["SECRET_KEY"] = "j-ITiFqDJMq2bqXLf3-DIg"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lacs.db"
app.secret_key = "secret key"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_vew = "login"
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Filtre personnalisé pour formater les dates en français
def format_date_fr(date_value, format_type="date"):
    if not date_value:
        return ""

    # Dictionnaire des mois en français
    mois_fr = {
        1: "janvier",
        2: "février",
        3: "mars",
        4: "avril",
        5: "mai",
        6: "juin",
        7: "juillet",
        8: "août",
        9: "septembre",
        10: "octobre",
        11: "novembre",
        12: "décembre",
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
