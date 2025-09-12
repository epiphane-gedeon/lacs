from flask import render_template, request, redirect, url_for, flash
from app import app, login_manager, db
from app.models import Utilisateur, Categorie, Article
from app.forms import ArticleForm, CategorieForm, InscriptionForm
from slugify import slugify


@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(user_id)


@app.route("/")
def home():
    articles = Article.query.order_by(Article.created_at.desc()).limit(3).all()
    return render_template("index.html", articles=articles)


@app.route("/inscription", methods=["GET", "POST"])
def inscription():
    form = InscriptionForm()
    if form.validate_on_submit():
        # Traiter l'inscription ici
        # utilisateur = Utilisateur(
        #     nom=form.nom.data,
        #     prenom=form.prenom.data,
        #     email=form.email.data,
        #     telephone=form.telephone.data,
        #     date_naissance=form.date_naissance.data,
        #     genre=form.genre.data,
        #     adresse=form.adresse.data,
        #     nom_parent=form.nom_parent.data,
        #     telephone_parent=form.telephone_parent.data,
        #     niveau_etude=form.niveau_etude.data,
        #     specialites=form.specialites.data,
        #     etablissement_actuel=form.etablissement_actuel.data,
        #     niveau_maths=form.niveau_maths.data,
        #     bulletin=form.bulletin.data,
        # )
        # db.session.add(utilisateur)
        # db.session.commit()
        # flash("Inscription réussie !", "success")
        return redirect(url_for("home"))
    return render_template("inscription.html", form=form)


@app.route("/add-article", methods=["GET", "POST"])
def add_article():
    form = ArticleForm()
    if form.validate_on_submit():
        # Créer le slug à partir du titre
        slug = slugify(form.titre.data)

        article = Article(
            titre=form.titre.data,
            slug=slug,
            contenu=form.contenu.data,
            categorie_id=form.categorie_id.data,
            auteur_id=1,  # Pour l'instant, on met 1 (à remplacer par current_user.id plus tard)
        )

        db.session.add(article)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("add-article.html", form=form)


@app.route("/add-categorie", methods=["GET", "POST"])
def add_categorie():
    form = CategorieForm()
    categories = Categorie.query.all()

    if form.validate_on_submit():
        categorie = Categorie(nom=form.nom.data, description=form.description.data)

        db.session.add(categorie)
        db.session.commit()

        return redirect(url_for("add_categorie"))

    return render_template("add-categorie.html", form=form, categories=categories)


@app.route("/article/<slug>")
def article_detail(slug):
    article = Article.query.filter_by(slug=slug).first_or_404()
    articles = Article.query.order_by(Article.created_at.desc()).limit(5).all()
    categories = Categorie.query.all()
    return render_template(
        "article_detail.html", article=article, articles=articles, categories=categories
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

    # Récupérer toutes les catégories pour les boutons de filtre
    categories = Categorie.query.all()

    return render_template(
        "actualites.html",
        articles=articles,
        categories=categories,
        categorie_actuelle=categorie_filter,
        search_query=search_query,
    )
