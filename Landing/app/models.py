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
    created_at = db.Column(db.Date, default=datetime.datetime.today())
    auteur_id = db.Column(db.Integer, db.ForeignKey("utilisateur.id"), nullable=False)
    auteur = db.relationship("Utilisateur", backref=db.backref("articles", lazy=True))
    categorie_id = db.Column(db.Integer, db.ForeignKey("categorie.id"), nullable=False)
    categorie = db.relationship("Categorie", backref=db.backref("articles", lazy=True))


class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.Date, default=datetime.datetime.today())


class Commentaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.Date, default=datetime.datetime.today())
    article_id = db.Column(db.Integer, db.ForeignKey("article.id"), nullable=False)
    # image_path=db.Column(db.String(200), nullable=True)
    # image_base64=db.Column(db.Text, nullable=True)
    # image_path=db.Column(db.String(200), nullable=True)
    # image_base64=db.Column(db.Text, nullable=True)
    article = db.relationship("Article", backref=db.backref("commentaires", lazy=True))
    utilisateur_id = db.Column(db.Integer, db.ForeignKey("utilisateur.id"), nullable=False)
    utilisateur = db.relationship("Utilisateur", backref=db.backref("commentaires", lazy=True))


class Eleve(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matricule = db.Column(db.String(20), nullable=False, unique=True)
    date_naissance = db.Column(db.Date, nullable=False)
    classe = db.Column(db.String(50), nullable=False)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey("utilisateur.id"), nullable=False)
    utilisateur = db.relationship("Utilisateur", backref=db.backref("eleve", uselist=False, lazy=True))
    parent_id = db.Column(db.Integer, db.ForeignKey("parent.id"), nullable=True)
    parent = db.relationship("Parent", backref=db.backref("enfants", lazy=True))


class Formateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code_formateur = db.Column(db.String(20), nullable=False, unique=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey("utilisateur.id"), nullable=False)
    utilisateur = db.relationship("Utilisateur", backref=db.backref("formateur", uselist=False, lazy=True))


class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code_parent = db.Column(db.String(20), nullable=False, unique=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey("utilisateur.id"), nullable=False)
    utilisateur = db.relationship("Utilisateur", backref=db.backref("parent", uselist=False, lazy=True))
