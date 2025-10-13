from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, login_manager, db, mail
from app.models import Utilisateur, Categorie, Article, Eleve, Parent, Inscription
from app.forms import (
    ArticleForm,
    CategorieForm,
    InscriptionForm,
    LoginForm,
    ContactForm,
    SimpleContactForm,
)
from app.utils import save_image, delete_image, save_document
from slugify import slugify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
import datetime


@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(user_id)


def generer_matricule():
    """Génère un matricule unique au format LACS-AA-XNNN"""
    annee_actuelle = datetime.datetime.now().year
    annee_courte = str(annee_actuelle)[-2:]  # Les 2 derniers chiffres de l'année

    # Trouver le dernier matricule de l'année courante
    prefix = f"LACS-{annee_courte}-"
    dernier_eleve = (
        Eleve.query.filter(Eleve.matricule.like(f"{prefix}%"))
        .order_by(Eleve.matricule.desc())
        .first()
    )

    if dernier_eleve:
        # Extraire la partie lettre-nombre (ex: A001)
        matricule_part = dernier_eleve.matricule.split("-")[2]  # A001
        lettre = matricule_part[0]  # A
        numero = int(matricule_part[1:])  # 001

        # Si le numéro atteint 999, passer à la lettre suivante
        if numero >= 999:
            if lettre == "Z":
                raise ValueError("Limite de matricules atteinte pour cette année")
            nouvelle_lettre = chr(ord(lettre) + 1)
            nouveau_numero = 1
        else:
            nouvelle_lettre = lettre
            nouveau_numero = numero + 1
    else:
        # Premier matricule de l'année
        nouvelle_lettre = "A"
        nouveau_numero = 1

    return f"LACS-{annee_courte}-{nouvelle_lettre}{nouveau_numero:03d}"


def generer_code_parent():
    """Génère un code parent unique au format PAR-YYYY-NNN"""
    annee_actuelle = datetime.datetime.now().year
    prefix = f"PAR-{annee_actuelle}-"

    dernier_parent = (
        Parent.query.filter(Parent.code_parent.like(f"{prefix}%"))
        .order_by(Parent.code_parent.desc())
        .first()
    )

    if dernier_parent:
        numero = int(dernier_parent.code_parent.split("-")[2]) + 1
    else:
        numero = 1

    return f"PAR-{annee_actuelle}-{numero:03d}"


@app.route("/", methods=["GET", "POST"])
def home():
    contact_form = SimpleContactForm()
    articles = Article.query.order_by(Article.created_at.desc()).limit(3).all()

    # Traitement du formulaire de contact depuis la page d'accueil
    if contact_form.validate_on_submit():
        try:
            sujet_email = f"[LACS Contact] {contact_form.subject.data}"

            corps_email = f"""
Nouvelle demande de contact depuis la page d'accueil du site LACS :

Informations du contact :
- Nom : {contact_form.lastName.data}
- Prénom : {contact_form.firstName.data}
- Email : {contact_form.email.data}
- Téléphone : {contact_form.phone.data}
- Sujet : {contact_form.subject.data}

Message :
{contact_form.message.data}

---
Ce message a été envoyé depuis le formulaire de contact de la page d'accueil du site LACS.
Vous pouvez répondre directement à l'adresse : {contact_form.email.data}
            """

            # Créer le message email
            msg = Message(
                subject=sujet_email,
                recipients=["lacsetudes@gmail.com"],
                body=corps_email,
                reply_to=contact_form.email.data,
            )

            # Tentative d'envoi avec fallback
            try:
                mail.send(msg)
                flash(
                    "Votre message a été envoyé avec succès ! Nous vous répondrons dans les plus brefs délais.",
                    "success",
                )
                return redirect(url_for("home"))

            except Exception as e:
                print(f"Erreur envoi email principal: {e}")
                try:
                    msg.recipients = ["egpouli@gmail.com"]
                    mail.send(msg)
                    flash(
                        "Votre message a été envoyé avec succès ! Nous vous répondrons dans les plus brefs délais.",
                        "success",
                    )
                    return redirect(url_for("home"))
                except Exception as e2:
                    print(f"Erreur envoi email fallback: {e2}")
                    flash(
                        "Une erreur s'est produite lors de l'envoi. Veuillez réessayer ou nous contacter directement.",
                        "error",
                    )

        except Exception as e:
            print(f"Erreur générale: {e}")
            flash("Une erreur s'est produite. Veuillez réessayer.", "error")

    return render_template("index.html", articles=articles, contact_form=contact_form)


@app.route("/inscription", methods=["GET", "POST"])
def inscription():
    form = InscriptionForm()

    print("Données du formulaire reçues:")
    print(request.form)
    print("Validité du formulaire:", form.validate())

    if not form.validate():
        print("ERREURS DE VALIDATION:")
        for field_name, field in form._fields.items():
            if field.errors:
                print(f"  - {field_name}: {field.errors}")
        print("Détails des champs:")
        for field_name, field in form._fields.items():
            print(
                f"  - {field_name}: valeur='{field.data}', validators={[v.__class__.__name__ for v in field.validators]}"
            )

    if form.validate_on_submit():
        print("Formulaire validé, traitement de l'inscription...")
        try:
            # 1. Vérifier si un parent avec ce téléphone existe déjà
            parent_existant = None
            utilisateur_parent = Utilisateur.query.filter_by(
                numero_telephone=form.telephone_parent.data
            ).first()

            if utilisateur_parent and hasattr(utilisateur_parent, "parent"):
                parent_existant = utilisateur_parent.parent

            # 2. Créer ou récupérer le parent
            if not parent_existant:
                # Créer un nouvel utilisateur pour le parent
                utilisateur_parent = Utilisateur(
                    nom=form.nom_parent.data,
                    prenom="",  # On n'a que le nom complet
                    numero_telephone=form.telephone_parent.data,
                    email=f"parent_{form.telephone_parent.data}@temp.lacs",  # Email temporaire
                    mot_de_passe=generate_password_hash(
                        "temp123"
                    ),  # Mot de passe temporaire
                    admin=False,
                )
                db.session.add(utilisateur_parent)
                db.session.flush()  # Pour obtenir l'ID

                # Créer le parent
                parent_existant = Parent(
                    code_parent=generer_code_parent(),
                    utilisateur_id=utilisateur_parent.id,
                )
                db.session.add(parent_existant)
                db.session.flush()

            # 3. Créer l'utilisateur élève
            utilisateur_eleve = Utilisateur(
                nom=form.nom.data,
                prenom=form.prenom.data,
                numero_telephone=form.telephone.data,
                email=form.email.data
                if form.email.data
                else f"eleve_{form.telephone.data}@temp.lacs",
                mot_de_passe=generate_password_hash(
                    "temp123"
                ),  # Mot de passe temporaire
                admin=False,
            )
            db.session.add(utilisateur_eleve)
            db.session.flush()

            # 4. Créer l'élève avec le matricule généré
            matricule = generer_matricule()
            eleve = Eleve(
                matricule=matricule,
                date_naissance=form.date_naissance.data,
                classe=form.niveau_etude.data,
                genre=form.genre.data,
                utilisateur_id=utilisateur_eleve.id,
                parent_id=parent_existant.id,
            )
            db.session.add(eleve)
            db.session.flush()

            # 5. Traitement des fichiers bulletins (optionnel)
            bulletin_paths = []
            if form.bulletin.data:
                print(f"Nombre de fichiers bulletins reçus: {len(form.bulletin.data)}")
                # Traiter chaque fichier bulletin
                for i, file in enumerate(form.bulletin.data):
                    print(
                        f"Fichier {i + 1}: filename='{file.filename}', content_type='{file.content_type}'"
                    )
                    if (
                        file
                        and hasattr(file, "filename")
                        and file.filename
                        and file.filename != ""
                    ):
                        # Utiliser save_document pour sauvegarder le fichier (PDF ou image)
                        result = save_document(file, "bulletins")
                        if result["success"]:
                            bulletin_paths.append(result["filename"])
                            print(f"✅ Bulletin sauvegardé: {result['filename']}")
                        else:
                            print(
                                f"❌ Erreur lors de la sauvegarde du bulletin: {result['error']}"
                            )
                            # Continuer même si un fichier échoue
                    else:
                        print(f"Fichier {i + 1} ignoré (vide ou invalide)")
            else:
                print("Aucun fichier bulletin reçu")

            # 6. Traiter les services sélectionnés
            services_selectionnes = (
                ",".join(form.services.data) if form.services.data else ""
            )

            # 7. Créer l'inscription
            inscription_record = Inscription(
                adresse=form.adresse.data,
                niveau_etude=form.niveau_etude.data,
                specialites=form.series.data if form.series.data else "",
                etablissement_actuel=form.etablissement_actuel.data,
                niveau_maths=form.niveau_maths.data,
                niveau_sp=form.niveau_sp.data,
                niveau_svt=form.niveau_svt.data,
                bulletin_paths=",".join(bulletin_paths),
                programme=form.programme.data,
                creneau=form.creneau.data,
                services=services_selectionnes,
                eleve_id=eleve.id,
            )
            db.session.add(inscription_record)

            # 8. Valider toutes les modifications
            db.session.commit()

            flash(f"Inscription réussie ! Matricule attribué : {matricule}", "success")
            return redirect(url_for("home"))

        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de l'inscription : {str(e)}", "error")

    return render_template("inscription.html", form=form)


@app.route("/apropos")
def apropos():
    return render_template("apropos.html")


@app.route("/phototheque")
def phototheque():
    # Categories de photos pour organiser la galerie
    categories = [
        {
            "id": "cours",
            "nom": "Cours et Formations",
            "description": "Moments forts de nos cours et formations",
            "photos": [
                {"nom": "Cours de mathématiques", "fichier": "logo.png"},
                {"nom": "Formation Python", "fichier": "logo.png"},
                {"nom": "Physique-Chimie", "fichier": "logo.png"},
                {"nom": "Travaux pratiques SVT", "fichier": "logo.png"},
                {"nom": "Séance de révisions", "fichier": "logo.png"},
                {"nom": "Atelier scientifique", "fichier": "logo.png"},
            ],
        },
        {
            "id": "evenements",
            "nom": "Événements",
            "description": "Événements spéciaux et activités du L.AC.S",
            "photos": [
                {"nom": "Journée portes ouvertes", "fichier": "logo.png"},
                {"nom": "Remise des prix", "fichier": "logo.png"},
                {"nom": "Conférence scientifique", "fichier": "logo.png"},
                {"nom": "Fête de fin d'année", "fichier": "logo.png"},
                {"nom": "Sortie pédagogique", "fichier": "logo.png"},
                {"nom": "Cérémonie de diplômes", "fichier": "logo.png"},
            ],
        },
        {
            "id": "etudiants",
            "nom": "Vie Étudiante",
            "description": "Moments de convivialité et réussites de nos élèves",
            "photos": [
                {"nom": "Groupe d'étude", "fichier": "logo.png"},
                {"nom": "Pause détente", "fichier": "logo.png"},
                {"nom": "Réussite au BAC", "fichier": "logo.png"},
                {"nom": "Nouveaux élèves", "fichier": "logo.png"},
                {"nom": "Équipe de projet", "fichier": "logo.png"},
                {"nom": "Moment convivial", "fichier": "logo.png"},
            ],
        },
        {
            "id": "installations",
            "nom": "Nos Installations",
            "description": "Découvrez nos espaces d'apprentissage",
            "photos": [
                {"nom": "Salle de cours principale", "fichier": "logo.png"},
                {"nom": "Laboratoire scientifique", "fichier": "logo.png"},
                {"nom": "Espace informatique", "fichier": "logo.png"},
                {"nom": "Bibliothèque", "fichier": "logo.png"},
                {"nom": "Salle de réunion", "fichier": "logo.png"},
                {"nom": "Espace détente", "fichier": "logo.png"},
            ],
        },
    ]

    return render_template("phototheque.html", categories=categories)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        try:
            # Préparer le contenu de l'email
            sujet_mapping = {
                "inscription": "Demande d'inscription",
                "information": "Demande d'information",
                "rdv": "Prise de rendez-vous",
                "pedagogie": "Questions pédagogiques",
                "partenariat": "Partenariat",
                "autre": "Autre demande",
            }

            sujet_email = f"[LACS Contact] {sujet_mapping.get(form.subject.data, 'Nouvelle demande')}"

            corps_email = f"""
Nouvelle demande de contact depuis le site LACS :

Informations du contact :
- Nom : {form.lastName.data}
- Prénom : {form.firstName.data}
- Email : {form.email.data}
- Téléphone : {form.phone.data or "Non renseigné"}
- Sujet : {sujet_mapping.get(form.subject.data, "Autre")}

Message :
{form.message.data}

---
Ce message a été envoyé depuis le formulaire de contact du site LACS.
Vous pouvez répondre directement à l'adresse : {form.email.data}
            """

            # Créer le message email
            msg = Message(
                subject=sujet_email,
                recipients=["egpouli@gmail.com"],  # Email principal
                body=corps_email,
                reply_to=form.email.data,
            )

            # Tentative d'envoi à l'email principal
            try:
                mail.send(msg)
                flash(
                    "Votre message a été envoyé avec succès ! Nous vous répondrons dans les plus brefs délais.",
                    "success",
                )
                return redirect(url_for("contact"))

            except Exception as e:
                print(f"Erreur envoi email principal: {e}")

                # Fallback : essayer avec l'email Gmail
                try:
                    msg.recipients = ["lacsetudes@gmail.com"]
                    mail.send(msg)
                    flash(
                        "Votre message a été envoyé avec succès ! Nous vous répondrons dans les plus brefs délais.",
                        "success",
                    )
                    return redirect(url_for("contact"))

                except Exception as e2:
                    print(f"Erreur envoi email fallback: {e2}")
                    flash(
                        "Une erreur s'est produite lors de l'envoi. Veuillez réessayer ou nous contacter directement.",
                        "error",
                    )

        except Exception as e:
            print(f"Erreur générale: {e}")
            flash("Une erreur s'est produite. Veuillez réessayer.", "error")

    return render_template("contact.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = Utilisateur.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.mot_de_passe, form.mot_de_passe.data):
            if not user.admin:
                flash(
                    "Accès refusé. Seuls les administrateurs peuvent se connecter.",
                    "error",
                )
                return render_template("login.html", form=form)

            login_user(user, remember=form.remember_me.data)
            flash(f"Connexion réussie ! Bienvenue {user.prenom}", "success")

            # Rediriger vers la page demandée ou vers l'accueil
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Email ou mot de passe incorrect", "error")

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Vous avez été déconnecté avec succès", "info")
    return redirect(url_for("home"))


@app.route("/add-article", methods=["GET", "POST"])
@login_required
def add_article():
    form = ArticleForm()
    if form.validate_on_submit():
        # Créer le slug à partir du titre
        slug = slugify(form.titre.data)

        # Gérer l'upload d'image
        image_path = None
        image_base64 = None

        if form.image.data:
            image_result = save_image(form.image.data, "images/articles")
            if image_result["success"]:
                image_path = image_result["filename"]
                image_base64 = image_result["base64"]
            else:
                flash(
                    f"Erreur lors de l'upload de l'image: {image_result['error']}",
                    "error",
                )
                return render_template("add-article.html", form=form)

        article = Article(
            titre=form.titre.data,
            slug=slug,
            contenu=form.contenu.data,
            categorie_id=form.categorie_id.data,
            auteur_id=current_user.id,
            image_path=image_path,
            image_base64=image_base64,
        )

        db.session.add(article)
        db.session.commit()

        flash("Article créé avec succès!", "success")
        return redirect(url_for("home"))

    return render_template("add-article.html", form=form)


@app.route("/add-categorie", methods=["GET", "POST"])
@login_required
def add_categorie():
    form = CategorieForm()
    categories = Categorie.query.all()

    if form.validate_on_submit():
        # Gérer l'upload d'image
        image_path = None
        image_base64 = None

        if form.image.data:
            image_result = save_image(form.image.data, "images/categories")
            if image_result["success"]:
                image_path = image_result["filename"]
                image_base64 = image_result["base64"]
            else:
                flash(
                    f"Erreur lors de l'upload de l'image: {image_result['error']}",
                    "error",
                )
                return render_template(
                    "add-categorie.html", form=form, categories=categories
                )

        categorie = Categorie(
            nom=form.nom.data,
            description=form.description.data,
            image_path=image_path,
            image_base64=image_base64,
        )

        db.session.add(categorie)
        db.session.commit()

        flash("Catégorie créée avec succès!", "success")
        return redirect(url_for("add_categorie"))

    return render_template("add-categorie.html", form=form, categories=categories)


@app.route("/article/<slug>")
def article_detail(slug):
    article = Article.query.filter_by(slug=slug).first_or_404()
    articles = Article.query.order_by(Article.created_at.desc()).limit(5).all()
    categories = Categorie.query.all()
    auteur = Utilisateur.query.get(article.auteur_id)
    return render_template(
        "article_detail.html",
        article=article,
        articles=articles,
        categories=categories,
        auteur=auteur,
    )


@app.route("/actualites")
def actualites():
    # Récupérer le numéro de page depuis l'URL (par défaut page 1)
    page = request.args.get("page", 1, type=int)

    # Récupérer la catégorie à filtrer (optionnel)
    categorie_filter = request.args.get("categorie", None)

    # Récupérer le terme de recherche (optionnel)
    search_query = request.args.get("search", "").strip()

    # Nombre d'articles par page
    per_page = 5  # Vous pouvez ajuster ce nombre

    # Construire la requête de base
    query = Article.query

    # Appliquer le filtre par catégorie si spécifié
    if categorie_filter and categorie_filter != "all":
        query = query.filter(Article.categorie.has(nom=categorie_filter))

    # Appliquer la recherche si un terme est fourni
    if search_query:
        query = query.filter(
            db.or_(
                Article.titre.contains(search_query),
                Article.contenu.contains(search_query),
            )
        )

    # Pagination avec tri par date de création (plus récent en premier)
    articles = query.order_by(Article.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    # dernier_article = Article.query.order_by(Article.created_at.desc()).first()

    dernier_article = articles.items[0] if articles.items else None

    # Récupérer toutes les catégories pour les boutons de filtre
    categories = Categorie.query.all()

    return render_template(
        "actualites.html",
        articles=articles,
        categories=categories,
        categorie_actuelle=categorie_filter,
        search_query=search_query,
        dernier_article=dernier_article,
    )


@app.route("/inscriptions")
@login_required
def liste_inscriptions():
    """Route pour afficher toutes les inscriptions (pour test/admin)"""
    inscriptions = Inscription.query.order_by(Inscription.created_at.desc()).all()
    return render_template("inscriptions.html", inscriptions=inscriptions)


@app.route("/bulletins/<int:eleve_id>")
@login_required
def voir_bulletins(eleve_id):
    """Route pour voir les bulletins d'un élève spécifique"""
    eleve = Eleve.query.get_or_404(eleve_id)
    inscription = Inscription.query.filter_by(eleve_id=eleve_id).first()

    bulletins = []
    if inscription and inscription.bulletin_paths:
        # Séparer les chemins des bulletins
        bulletin_paths = inscription.bulletin_paths.split(",")
        for path in bulletin_paths:
            if path.strip():  # Vérifier que le chemin n'est pas vide
                bulletins.append(
                    {
                        "path": path.strip(),
                        "filename": path.split("/")[
                            -1
                        ],  # Nom du fichier sans le chemin
                        "is_pdf": path.lower().endswith(".pdf"),
                    }
                )

    return render_template(
        "bulletins.html", eleve=eleve, inscription=inscription, bulletins=bulletins
    )


@app.route("/admin")
def admin_dashboard():
    return render_template("admin/index.html")
