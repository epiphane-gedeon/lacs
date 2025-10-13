from app import db
import datetime
from flask_login import UserMixin


class Utilisateur(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    numero_telephone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    mot_de_passe = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.Date, default=datetime.datetime.today())
    admin = db.Column(db.Boolean, default=False)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    contenu = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(200), nullable=True)
    image_base64 = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.Date, default=datetime.datetime.today())
    auteur_id = db.Column(db.Integer, db.ForeignKey("utilisateur.id"), nullable=False)
    auteur = db.relationship("Utilisateur", backref=db.backref("articles", lazy=True))
    categorie_id = db.Column(db.Integer, db.ForeignKey("categorie.id"), nullable=False)
    categorie = db.relationship("Categorie", backref=db.backref("articles", lazy=True))


class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(200), nullable=True)
    image_base64 = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.Date, default=datetime.datetime.today())


class Commentaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.Date, default=datetime.datetime.today())
    article_id = db.Column(db.Integer, db.ForeignKey("article.id"), nullable=False)
    article = db.relationship("Article", backref=db.backref("commentaires", lazy=True))
    utilisateur_id = db.Column(
        db.Integer, db.ForeignKey("utilisateur.id"), nullable=False
    )
    utilisateur = db.relationship(
        "Utilisateur", backref=db.backref("commentaires", lazy=True)
    )


class Eleve(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matricule = db.Column(db.String(20), nullable=False, unique=True)
    date_naissance = db.Column(db.Date, nullable=False)
    classe = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(10), nullable=False)
    utilisateur_id = db.Column(
        db.Integer, db.ForeignKey("utilisateur.id"), nullable=False
    )
    utilisateur = db.relationship(
        "Utilisateur", backref=db.backref("eleve", uselist=False, lazy=True)
    )
    parent_id = db.Column(db.Integer, db.ForeignKey("parent.id"), nullable=True)
    parent = db.relationship("Parent", backref=db.backref("enfants", lazy=True))


class Formateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code_formateur = db.Column(db.String(20), nullable=False, unique=True)
    utilisateur_id = db.Column(
        db.Integer, db.ForeignKey("utilisateur.id"), nullable=False
    )
    utilisateur = db.relationship(
        "Utilisateur", backref=db.backref("formateur", uselist=False, lazy=True)
    )


class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code_parent = db.Column(db.String(20), nullable=False, unique=True)
    utilisateur_id = db.Column(
        db.Integer, db.ForeignKey("utilisateur.id"), nullable=False
    )
    utilisateur = db.relationship(
        "Utilisateur", backref=db.backref("parent", uselist=False, lazy=True)
    )


class Inscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adresse = db.Column(db.String(200), nullable=False)
    niveau_etude = db.Column(db.String(50), nullable=False)
    specialites = db.Column(db.String(100), nullable=True)
    etablissement_actuel = db.Column(db.String(200), nullable=False)
    niveau_maths = db.Column(db.String(50), nullable=False)
    niveau_sp = db.Column(db.String(50), nullable=False)
    niveau_svt = db.Column(db.String(50), nullable=False)
    bulletin_paths = db.Column(
        db.Text, nullable=True
    )  # Stocke les chemins des fichiers séparés par des virgules
    programme = db.Column(db.String(50), nullable=False)
    creneau = db.Column(db.String(50), nullable=True)
    services = db.Column(
        db.Text, nullable=True
    )  # Stocke les services sélectionnés séparés par des virgules
    attentes_lacs = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.Date, default=datetime.datetime.today())
    eleve_id = db.Column(db.Integer, db.ForeignKey("eleve.id"), nullable=True)
    eleve = db.relationship(
        "Eleve", backref=db.backref("inscription", uselist=False, lazy=True)
    )
