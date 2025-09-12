from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, DateField, EmailField, RadioField, FileField, TelField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length
from app.models import Categorie


class ArticleForm(FlaskForm):
    titre = StringField("Titre", validators=[DataRequired(), Length(min=5, max=100)])
    contenu = TextAreaField("Contenu", validators=[DataRequired()])
    categorie_id = SelectField("Catégorie", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Publier l'article")

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.categorie_id.choices = [(c.id, c.nom) for c in Categorie.query.all()]


class CategorieForm(FlaskForm):
    nom = StringField(
        "Nom de la catégorie", validators=[DataRequired(), Length(min=3, max=50)]
    )
    description = TextAreaField("Description", validators=[Length(max=200)])
    submit = SubmitField("Créer la catégorie")

class InscriptionForm(FlaskForm):
    nom = StringField("Nom", validators=[DataRequired(), Length(min=2, max=100)],render_kw={'class': 'form-input'})
    prenom = StringField("Prénom", validators=[DataRequired(), Length(min=2, max=100)],render_kw={'class': 'form-input'})
    email = EmailField("Email", validators=[Length(max=100)],render_kw={'class': 'form-input'})
    telephone = TelField("Numéro de téléphone", validators=[DataRequired(),Length(min=8)],render_kw={'class': 'form-input'})
    date_naissance = DateField("Date de naissance", validators=[DataRequired()], format="%Y-%m-%d",render_kw={'class': 'form-input'})
    genre=SelectField("Genre", choices=[('', 'Choisir'),('M', 'Masculin'), ('F', 'Féminin')], validators=[DataRequired()],render_kw={'class': 'form-input form-select'})
    adresse = StringField("Adresse (Quartier)", validators=[DataRequired(), Length(min=5, max=200)],render_kw={'class': 'form-input'})
    nom_parent = StringField("Nom du parent", validators=[DataRequired(), Length(min=2, max=100)],render_kw={'class': 'form-input'})
    telephone_parent = TelField("Téléphone du parent", validators=[DataRequired(), Length(min=8)],render_kw={'class': 'form-input'})
    niveau_etude = SelectField("Niveau d'étude", choices=[('', 'Choisir'), ('quatrieme', 'Quatrième'), ('troisieme', 'Troisième'), ('seconde', 'Seconde'), ('premiere', 'Première'), ('terminale', 'Terminale')], validators=[DataRequired()],render_kw={'class': 'form-input form-select'})
    series= RadioField( "Séries (Seulement pour Première/Terminale)", choices=[('c', 'C'), ('d', 'D')], validators=[DataRequired()])
    validators=[DataRequired()]
    etablissement_actuel=StringField("Établissement actuel", validators=[DataRequired(), Length(min=2, max=200)],render_kw={'class': 'form-input'})
    niveau_maths=SelectField("Niveau en mathématiques", choices=[('', 'Evaluez votre niveau'), ('excellent', 'Excellent (16-20/20)'), ('bon', 'Bon (14-16/20)'), ('moyen', 'Moyen (12-14/20)'), ('faible', 'Faible (10-12/20)'), ('difficile', 'Difficile (moins de 10/20)')], validators=[DataRequired()],render_kw={'class': 'form-input form-select'})
    niveau_sp=SelectField("Niveau en Sciences Physiques", choices=[('', 'Evaluez votre niveau'), ('excellent', 'Excellent (16-20/20)'), ('bon', 'Bon (14-16/20)'), ('moyen', 'Moyen (12-14/20)'), ('faible', 'Faible (10-12/20)'), ('difficile', 'Difficile (moins de 10/20)')], validators=[DataRequired()],render_kw={'class': 'form-input form-select'})
    bulletin= FileField("Bulletin scolaire (optionnel)", validators=[DataRequired(), Length(max=200)],render_kw={'class': 'form-input'})

    # mot_de_passe = StringField("Mot de passe", validators=[DataRequired(), Length(min=6, max=100)])
    submit = SubmitField("Confirmer l'inscription")
