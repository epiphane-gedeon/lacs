from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    SubmitField,
    DateField,
    EmailField,
    RadioField,
    FileField,
    TelField,
    PasswordField,
    BooleanField,
    MultipleFileField,
    SelectMultipleField,
    widgets,
)
from flask_wtf.file import FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length
from app.models import Categorie


class ArticleForm(FlaskForm):
    titre = StringField("Titre", validators=[DataRequired(), Length(min=5, max=100)])
    contenu = TextAreaField("Contenu", validators=[DataRequired()], default="vide")
    categorie_id = SelectField("Catégorie", coerce=int, validators=[DataRequired()])
    image = FileField(
        "Image de l'article",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png", "gif", "webp"],
                "Seuls les fichiers image sont autorisés (JPG, PNG, GIF, WEBP)!",
            )
        ],
        render_kw={
            "class": "form-control",
            "accept": ".jpg,.jpeg,.png,.gif,.webp",
            "onchange": 'previewImage(this, "article-preview")',
        },
    )
    submit = SubmitField("Publier l'article")

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.categorie_id.choices = [(c.id, c.nom) for c in Categorie.query.all()]


class CategorieForm(FlaskForm):
    nom = StringField(
        "Nom de la catégorie", validators=[DataRequired(), Length(min=3, max=50)]
    )
    description = TextAreaField("Description", validators=[Length(max=200)])
    image = FileField(
        "Image de la catégorie",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png", "gif", "webp"],
                "Seuls les fichiers image sont autorisés (JPG, PNG, GIF, WEBP)!",
            )
        ],
        render_kw={
            "class": "form-control",
            "accept": ".jpg,.jpeg,.png,.gif,.webp",
            "onchange": 'previewImage(this, "categorie-preview")',
        },
    )
    submit = SubmitField("Créer la catégorie")


class InscriptionForm(FlaskForm):
    nom = StringField(
        "Nom",
        validators=[DataRequired(), Length(min=2, max=100)],
        render_kw={"class": "form-input"},
    )
    prenom = StringField(
        "Prénom",
        validators=[DataRequired(), Length(min=2, max=100)],
        render_kw={"class": "form-input"},
    )
    email = EmailField(
        "Email", validators=[Length(max=100)], render_kw={"class": "form-input"}
    )
    telephone = TelField(
        "Numéro de téléphone",
        validators=[],
        render_kw={"class": "form-input"},
    )
    date_naissance = DateField(
        "Date de naissance",
        validators=[DataRequired()],
        format="%Y-%m-%d",
        render_kw={"class": "form-input"},
    )
    genre = SelectField(
        "Genre",
        choices=[("", "Choisir"), ("M", "Masculin"), ("F", "Féminin")],
        validators=[DataRequired()],
        render_kw={"class": "form-input form-select"},
    )
    adresse = StringField(
        "Adresse (Quartier)",
        validators=[DataRequired(), Length(min=5, max=200)],
        render_kw={"class": "form-input"},
    )
    nom_parent = StringField(
        "Nom du parent",
        validators=[DataRequired(), Length(min=2, max=100)],
        render_kw={"class": "form-input"},
    )
    telephone_parent = TelField(
        "Téléphone du parent (Whatsapp)",
        validators=[DataRequired(), Length(min=8)],
        render_kw={"class": "form-input"},
    )
    niveau_etude = SelectField(
        "Niveau d'étude",
        choices=[
            ("", "Choisir"),
            ("quatrieme", "Quatrième"),
            ("troisieme", "Troisième"),
            ("seconde", "Seconde"),
            ("premiere", "Première"),
            ("terminale", "Terminale"),
        ],
        validators=[DataRequired()],
        render_kw={"class": "form-input form-select"},
    )
    series = RadioField(
        "Séries (Seulement pour Première/Terminale)",
        choices=[("", "Non applicable"), ("c", "C"), ("d", "D")],
        validators=[],
        default="",
    )
    etablissement_actuel = StringField(
        "Établissement de provenance",
        validators=[DataRequired(), Length(min=2, max=200)],
        render_kw={"class": "form-input"},
    )
    niveau_maths = SelectField(
        "Niveau en mathématiques",
        choices=[
            ("", "Evaluez votre niveau"),
            ("excellent", "Excellent (16-20/20)"),
            ("bon", "Bon (14-16/20)"),
            ("moyen", "Moyen (12-14/20)"),
            ("faible", "Faible (10-12/20)"),
            ("difficile", "Difficile (moins de 10/20)"),
        ],
        validators=[DataRequired()],
        render_kw={"class": "form-input form-select"},
    )
    niveau_sp = SelectField(
        "Niveau en Sciences Physiques",
        choices=[
            ("", "Evaluez votre niveau"),
            ("excellent", "Excellent (16-20/20)"),
            ("bon", "Bon (14-16/20)"),
            ("moyen", "Moyen (12-14/20)"),
            ("faible", "Faible (10-12/20)"),
            ("difficile", "Difficile (moins de 10/20)"),
        ],
        validators=[DataRequired()],
        render_kw={"class": "form-input form-select"},
    )
    niveau_svt = SelectField(
        "Niveau en SVT",
        choices=[
            ("", "Evaluez votre niveau"),
            ("excellent", "Excellent (16-20/20)"),
            ("bon", "Bon (14-16/20)"),
            ("moyen", "Moyen (12-14/20)"),
            ("faible", "Faible (10-12/20)"),
            ("difficile", "Difficile (moins de 10/20)"),
        ],
        validators=[DataRequired()],
        render_kw={"class": "form-input form-select"},
    )
    bulletin = MultipleFileField(
        "Bulletin scolaire",
        validators=[
            FileAllowed(
                ["png", "jpg", "jpeg", "pdf"],
                "Seuls les fichiers PNG, JPG et PDF sont autorisés!",
            )
        ],
        render_kw={
            "class": "file-input",
            "accept": ".png,.jpg,.jpeg,.pdf",
            "multiple": True,
        },
    )
    programme = RadioField(
        "Type de programme",
        choices=[
            ("standard", "Standard"),
            ("ligne", "En ligne"),
            ("domicile", "A domicile"),
        ],
        validators=[DataRequired()],
    )
    creneau = SelectField(
        "Créneau préféré",
        choices=[
            ("", "Choisir"),
            ("semaine_apres_midi", " Semaine Après-midi (14h-18h)"),
            ("semaine_soir", "Semaine Soir (18h-20h)"),
            ("samedi_matin", "Samedi (8h-12h)"),
            ("samedi_apres_midi", "Samedi (14h-18h)"),
        ],
        validators=[],
        render_kw={"class": "form-input form-select"},
    )
    services = SelectMultipleField(
        "Type de programme",
        choices=[
            ("bureautique", "Bureautique"),
            ("python", "Initiation à la programmation avec Python"),
            ("scolaire", "Accompagnement scolaire (Maths, Physique, SVT)"),
        ],
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False),
        validators=[],
    )
    attentes_lacs = TextAreaField(
        "Quelles sont vos attentes vis-à-vis de LACS ?",
        validators=[Length(max=500)],
        render_kw={"class": "form-textarea", "rows": 4},
    )

    # mot_de_passe = StringField("Mot de passe", validators=[DataRequired(), Length(min=6, max=100)])
    submit = SubmitField("Confirmer l'inscription  ")


class LoginForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Votre email"},
    )
    mot_de_passe = PasswordField(
        "Mot de passe",
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Votre mot de passe"},
    )
    remember_me = BooleanField("Se souvenir de moi")
    submit = SubmitField("Se connecter")


class ContactForm(FlaskForm):
    firstName = StringField(
        "Prénom",
        validators=[DataRequired(), Length(min=2, max=50)],
        render_kw={"class": "form-input", "id": "firstName"},
    )
    lastName = StringField(
        "Nom",
        validators=[DataRequired(), Length(min=2, max=50)],
        render_kw={"class": "form-input", "id": "lastName"},
    )
    email = EmailField(
        "Email",
        validators=[DataRequired()],
        render_kw={"class": "form-input", "id": "email"},
    )
    phone = TelField(
        "Téléphone",
        validators=[Length(max=20)],
        render_kw={"class": "form-input", "id": "phone"},
    )
    subject = SelectField(
        "Sujet",
        choices=[
            ("", "Choisissez un sujet"),
            ("inscription", "Demande d'inscription"),
            ("information", "Demande d'information"),
            ("rdv", "Prise de rendez-vous"),
            ("pedagogie", "Questions pédagogiques"),
            ("partenariat", "Partenariat"),
            ("autre", "Autre"),
        ],
        validators=[DataRequired()],
        render_kw={"class": "form-input form-select", "id": "subject"},
    )
    message = TextAreaField(
        "Message",
        validators=[DataRequired(), Length(min=10, max=1000)],
        render_kw={
            "class": "form-input form-textarea",
            "id": "message",
            "rows": "5",
            "placeholder": "Décrivez votre demande en détail...",
        },
    )
    consent = BooleanField(
        "J'accepte que mes données personnelles soient utilisées pour répondre à ma demande.",
        validators=[DataRequired()],
        render_kw={"class": "form-checkbox", "id": "consent"},
    )
    submit = SubmitField("Envoyer le message")


class SimpleContactForm(FlaskForm):
    """Formulaire de contact simplifié pour la page d'accueil"""

    firstName = StringField(
        "Prénom",
        validators=[DataRequired(), Length(min=2, max=50)],
        render_kw={"placeholder": "Prénom", "id": "firstName"},
    )
    lastName = StringField(
        "Nom",
        validators=[DataRequired(), Length(min=2, max=50)],
        render_kw={"placeholder": "Nom de famille", "id": "lastName"},
    )
    email = EmailField(
        "Email",
        validators=[DataRequired()],
        render_kw={"placeholder": "Adresse email", "id": "email"},
    )
    phone = TelField(
        "Téléphone",
        validators=[DataRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "Numéro de téléphone", "id": "phone"},
    )
    subject = StringField(
        "Sujet",
        validators=[DataRequired(), Length(min=5, max=100)],
        render_kw={"placeholder": "Sujet de votre message", "id": "subject"},
    )
    message = TextAreaField(
        "Message",
        validators=[DataRequired(), Length(min=10, max=1000)],
        render_kw={"placeholder": "Votre message", "rows": "5", "id": "message"},
    )
    privacy = BooleanField(
        "J'accepte la Politique de Confidentialité et autorise le traitement de mes données personnelles",
        validators=[DataRequired()],
        render_kw={"id": "privacy"},
    )
    submit = SubmitField("Envoyer le message", render_kw={"class": "btn-submit"})
