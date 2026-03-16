"""
routes.py — Tous les endpoints de l'API LACS
"""

from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import and_, delete, insert
from sqlalchemy.orm import Session

from app import app
from app.auth import (
    create_access_token,
    get_current_user,
    hash_password,
    require_roles,
    verify_password,
)
from app.database import get_db
from app.models import (
    Absence,
    Administrateur,
    Annonce,
    AnneeScolaire,
    Classe,
    Cours,
    Devoir,
    Directeur,
    Eleve,
    EmploiDuTemps,
    Evaluation,
    Formateur,
    Inscription,
    Matiere,
    Note,
    Notification,
    Parent,
    ResponsablePedagogique,
    Soumission,
    SupportPedagogique,
    Utilisateur,
    formateur_classe,
    formateur_matiere,
    parent_eleve,
)
from app.schema import (
    AbsenceCreate,
    AbsenceResponse,
    AbsenceUpdate,
    AnnonceCreate,
    AnnonceResponse,
    AnnonceUpdate,
    AnneeScolaireCreate,
    AnneeScolaireResponse,
    ClasseCreate,
    ClasseResponse,
    ClasseUpdate,
    CoursCreate,
    CoursResponse,
    CoursUpdate,
    DevoirCreate,
    DevoirResponse,
    DevoirUpdate,
    EleveCreate,
    EleveResponse,
    EleveUpdate,
    EmploiDuTempsCreate,
    EmploiDuTempsResponse,
    EmploiDuTempsUpdate,
    EvaluationCreate,
    EvaluationResponse,
    EvaluationUpdate,
    FormateurAttribuerClasse,
    FormateurAttribuerMatiere,
    FormateurCreate,
    FormateurResponse,
    InscriptionCreate,
    InscriptionReinscription,
    InscriptionResponse,
    InscriptionUpdate,
    MatiereCreate,
    MatiereResponse,
    MatiereUpdate,
    NoteBatch,
    NoteBatchItem,
    NoteCreate,
    NoteResponse,
    NoteUpdate,
    NotificationResponse,
    ParentCreate,
    ParentResponse,
    ParentUpdate,
    RoleCreate,
    RoleResponse,
    SoumissionCorriger,
    SoumissionCreate,
    SoumissionResponse,
    SupportPedagogiqueCreate,
    SupportPedagogiqueResponse,
    Token,
    UtilisateurCreate,
    UtilisateurLogin,
    UtilisateurResetPassword,
    UtilisateurResponse,
    UtilisateurUpdate,
)


# ===========================================================================
# Utilitaires internes
# ===========================================================================


def _get_or_404(db: Session, model, id, label: str):
    obj = db.get(model, id)
    if not obj:
        raise HTTPException(status_code=404, detail=f"{label} introuvable")
    return obj


def _create_utilisateur(
    db: Session, name: str, firstname: str, email: str, password: str
) -> Utilisateur:
    if db.query(Utilisateur).filter(Utilisateur.email == email).first():
        raise HTTPException(status_code=409, detail="Email déjà utilisé")
    now = datetime.now(timezone.utc)
    user = Utilisateur(
        name=name,
        firstname=firstname,
        email=email,
        password=hash_password(password),
        created_at=now,
        updated_at=now,
    )
    db.add(user)
    db.flush()
    return user


# ===========================================================================
# Health-check
# ===========================================================================


@app.get("/", tags=["health"])
def health():
    return {"status": "ok", "service": "LACS API"}


# ===========================================================================
# AUTH
# ===========================================================================


@app.post("/auth/login", response_model=Token, tags=["auth"])
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Utilisateur).filter(Utilisateur.email == form.username).first()
    if not user or not verify_password(form.password, user.password):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    token = create_access_token({"sub": str(user.id)})
    return Token(access_token=token)


@app.get("/auth/me", response_model=UtilisateurResponse, tags=["auth"])
def me(current_user: Utilisateur = Depends(get_current_user)):
    return current_user


# ===========================================================================
# ANNÉES SCOLAIRES
# ===========================================================================


@app.get(
    "/annees-scolaires/",
    response_model=List[AnneeScolaireResponse],
    tags=["annees-scolaires"],
)
def list_annees(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(AnneeScolaire).order_by(AnneeScolaire.name).all()


@app.post(
    "/annees-scolaires/",
    response_model=AnneeScolaireResponse,
    status_code=201,
    tags=["annees-scolaires"],
)
def create_annee(
    body: AnneeScolaireCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur", "directeur")),
):
    annee = AnneeScolaire(name=body.name, is_active=False)
    db.add(annee)
    db.commit()
    db.refresh(annee)
    return annee


@app.get(
    "/annees-scolaires/{id}",
    response_model=AnneeScolaireResponse,
    tags=["annees-scolaires"],
)
def get_annee(id: UUID, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return _get_or_404(db, AnneeScolaire, id, "Année scolaire")


@app.put(
    "/annees-scolaires/{id}",
    response_model=AnneeScolaireResponse,
    tags=["annees-scolaires"],
)
def update_annee(
    id: UUID,
    body: AnneeScolaireCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur", "directeur")),
):
    annee = _get_or_404(db, AnneeScolaire, id, "Année scolaire")
    annee.name = body.name
    db.commit()
    db.refresh(annee)
    return annee


@app.delete("/annees-scolaires/{id}", status_code=204, tags=["annees-scolaires"])
def delete_annee(
    id: UUID, db: Session = Depends(get_db), _=Depends(require_roles("administrateur"))
):
    annee = _get_or_404(db, AnneeScolaire, id, "Année scolaire")
    if annee.inscriptions:
        raise HTTPException(
            status_code=409,
            detail="Impossible de supprimer une année avec des inscriptions",
        )
    db.delete(annee)
    db.commit()


@app.patch(
    "/annees-scolaires/{id}/activer",
    response_model=AnneeScolaireResponse,
    tags=["annees-scolaires"],
)
def activer_annee(
    id: UUID,
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur", "directeur")),
):
    # Désactiver toutes les autres
    db.query(AnneeScolaire).update({AnneeScolaire.is_active: False})
    annee = _get_or_404(db, AnneeScolaire, id, "Année scolaire")
    annee.is_active = True
    db.commit()
    db.refresh(annee)
    return annee


def _get_annee_active(db: Session) -> AnneeScolaire:
    annee = db.query(AnneeScolaire).filter(AnneeScolaire.is_active == True).first()
    if not annee:
        raise HTTPException(status_code=400, detail="Aucune année scolaire active")
    return annee


# ===========================================================================
# UTILISATEURS
# ===========================================================================


@app.get(
    "/utilisateurs/", response_model=List[UtilisateurResponse], tags=["utilisateurs"]
)
def list_utilisateurs(
    db: Session = Depends(get_db), _=Depends(require_roles("administrateur"))
):
    return db.query(Utilisateur).all()


@app.post(
    "/utilisateurs/",
    response_model=UtilisateurResponse,
    status_code=201,
    tags=["utilisateurs"],
)
def create_utilisateur(
    body: UtilisateurCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur")),
):
    user = _create_utilisateur(db, body.name, body.firstname, body.email, body.password)
    db.commit()
    db.refresh(user)
    return user


@app.get(
    "/utilisateurs/{id}", response_model=UtilisateurResponse, tags=["utilisateurs"]
)
def get_utilisateur(
    id: UUID, db: Session = Depends(get_db), _=Depends(require_roles("administrateur"))
):
    return _get_or_404(db, Utilisateur, id, "Utilisateur")


@app.put(
    "/utilisateurs/{id}", response_model=UtilisateurResponse, tags=["utilisateurs"]
)
def update_utilisateur(
    id: UUID,
    body: UtilisateurUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur")),
):
    user = _get_or_404(db, Utilisateur, id, "Utilisateur")
    if body.name is not None:
        user.name = body.name
    if body.firstname is not None:
        user.firstname = body.firstname
    if body.email is not None:
        existing = (
            db.query(Utilisateur)
            .filter(Utilisateur.email == body.email, Utilisateur.id != id)
            .first()
        )
        if existing:
            raise HTTPException(status_code=409, detail="Email déjà utilisé")
        user.email = body.email
    user.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(user)
    return user


@app.delete("/utilisateurs/{id}", status_code=204, tags=["utilisateurs"])
def delete_utilisateur(
    id: UUID, db: Session = Depends(get_db), _=Depends(require_roles("administrateur"))
):
    user = _get_or_404(db, Utilisateur, id, "Utilisateur")
    db.delete(user)
    db.commit()


@app.patch("/utilisateurs/{id}/reset-password", status_code=204, tags=["utilisateurs"])
def reset_password(
    id: UUID,
    body: UtilisateurResetPassword,
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur")),
):
    user = _get_or_404(db, Utilisateur, id, "Utilisateur")
    user.password = hash_password(body.new_password)
    user.updated_at = datetime.now(timezone.utc)
    db.commit()


# ===========================================================================
# ÉLÈVES  (profils permanents)
# ===========================================================================


@app.get("/eleves/", response_model=List[EleveResponse], tags=["eleves"])
def list_eleves(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Eleve).all()


@app.post("/eleves/", response_model=EleveResponse, status_code=201, tags=["eleves"])
def create_eleve(
    body: EleveCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur")),
):
    if db.query(Eleve).filter(Eleve.matricule == body.matricule).first():
        raise HTTPException(status_code=409, detail="Matricule déjà utilisé")
    user = _create_utilisateur(db, body.name, body.firstname, body.email, body.password)
    eleve = Eleve(user_id=user.id, matricule=body.matricule)
    db.add(eleve)
    db.commit()
    db.refresh(eleve)
    return eleve


@app.get("/eleves/{id}", response_model=EleveResponse, tags=["eleves"])
def get_eleve(id: UUID, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return _get_or_404(db, Eleve, id, "Élève")


@app.put("/eleves/{id}", response_model=EleveResponse, tags=["eleves"])
def update_eleve(
    id: UUID,
    body: EleveUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur")),
):
    eleve = _get_or_404(db, Eleve, id, "Élève")
    if body.matricule is not None:
        eleve.matricule = body.matricule
    db.commit()
    db.refresh(eleve)
    return eleve


@app.delete("/eleves/{id}", status_code=204, tags=["eleves"])
def delete_eleve(
    id: UUID, db: Session = Depends(get_db), _=Depends(require_roles("administrateur"))
):
    eleve = _get_or_404(db, Eleve, id, "Élève")
    if eleve.inscriptions:
        raise HTTPException(
            status_code=409,
            detail="Impossible de supprimer un élève avec des inscriptions",
        )
    db.delete(eleve)
    db.commit()


@app.get(
    "/eleves/{id}/inscriptions",
    response_model=List[InscriptionResponse],
    tags=["eleves"],
)
def get_inscriptions_eleve(
    id: UUID, db: Session = Depends(get_db), _=Depends(get_current_user)
):
    _get_or_404(db, Eleve, id, "Élève")
    return db.query(Inscription).filter(Inscription.eleve_id == id).all()


@app.get("/eleves/{id}/notes", response_model=List[NoteResponse], tags=["eleves"])
def get_notes_eleve(
    id: UUID,
    annee_scolaire_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _get_or_404(db, Eleve, id, "Élève")
    q = db.query(Note).filter(Note.eleve_id == id)
    if annee_scolaire_id:
        q = q.join(Evaluation).filter(Evaluation.annee_scolaire_id == annee_scolaire_id)
    return q.all()


# ===========================================================================
# INSCRIPTIONS  (pivot annuel)
# ===========================================================================


@app.get(
    "/inscriptions/", response_model=List[InscriptionResponse], tags=["inscriptions"]
)
def list_inscriptions(
    annee_scolaire_id: Optional[UUID] = None,
    eleve_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    q = db.query(Inscription)
    if annee_scolaire_id:
        q = q.filter(Inscription.annee_scolaire_id == annee_scolaire_id)
    if eleve_id:
        q = q.filter(Inscription.eleve_id == eleve_id)
    return q.all()


@app.post(
    "/inscriptions/",
    response_model=InscriptionResponse,
    status_code=201,
    tags=["inscriptions"],
)
def create_inscription(
    body: InscriptionCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur")),
):
    _get_or_404(db, Eleve, body.eleve_id, "Élève")
    _get_or_404(db, AnneeScolaire, body.annee_scolaire_id, "Année scolaire")
    existing = (
        db.query(Inscription)
        .filter(
            Inscription.eleve_id == body.eleve_id,
            Inscription.annee_scolaire_id == body.annee_scolaire_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=409, detail="Cet élève est déjà inscrit pour cette année"
        )
    insc = Inscription(
        eleve_id=body.eleve_id,
        annee_scolaire_id=body.annee_scolaire_id,
        classe_id=body.classe_id,
        is_ancien=body.is_ancien,
        date_inscription=datetime.now(timezone.utc),
    )
    db.add(insc)
    db.commit()
    db.refresh(insc)
    return insc


@app.post(
    "/inscriptions/reinscription",
    response_model=InscriptionResponse,
    status_code=201,
    tags=["inscriptions"],
)
def reinscription(
    body: InscriptionReinscription,
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur")),
):
    _get_or_404(db, Eleve, body.eleve_id, "Élève")
    _get_or_404(db, AnneeScolaire, body.annee_scolaire_id, "Année scolaire cible")
    existing = (
        db.query(Inscription)
        .filter(
            Inscription.eleve_id == body.eleve_id,
            Inscription.annee_scolaire_id == body.annee_scolaire_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=409, detail="Cet élève est déjà inscrit pour cette année"
        )
    insc = Inscription(
        eleve_id=body.eleve_id,
        annee_scolaire_id=body.annee_scolaire_id,
        classe_id=body.classe_id,
        is_ancien=True,
        date_inscription=datetime.now(timezone.utc),
    )
    db.add(insc)
    db.commit()
    db.refresh(insc)
    return insc


@app.get(
    "/inscriptions/{id}", response_model=InscriptionResponse, tags=["inscriptions"]
)
def get_inscription(
    id: UUID, db: Session = Depends(get_db), _=Depends(get_current_user)
):
    return _get_or_404(db, Inscription, id, "Inscription")


@app.put(
    "/inscriptions/{id}", response_model=InscriptionResponse, tags=["inscriptions"]
)
def update_inscription(
    id: UUID,
    body: InscriptionUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur")),
):
    insc = _get_or_404(db, Inscription, id, "Inscription")
    if body.classe_id is not None:
        _get_or_404(db, Classe, body.classe_id, "Classe")
        insc.classe_id = body.classe_id
    db.commit()
    db.refresh(insc)
    return insc


@app.delete("/inscriptions/{id}", status_code=204, tags=["inscriptions"])
def delete_inscription(
    id: UUID, db: Session = Depends(get_db), _=Depends(require_roles("administrateur"))
):
    insc = _get_or_404(db, Inscription, id, "Inscription")
    db.delete(insc)
    db.commit()


# ===========================================================================
# CLASSES
# ===========================================================================


@app.get("/classes/", response_model=List[ClasseResponse], tags=["classes"])
def list_classes(
    annee_scolaire_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    q = db.query(Classe)
    if annee_scolaire_id:
        q = q.filter(Classe.annee_scolaire_id == annee_scolaire_id)
    classes = q.all()
    result = []
    for c in classes:
        resp = ClasseResponse.model_validate(c)
        resp.effectif = len(c.inscriptions)
        result.append(resp)
    return result


@app.post("/classes/", response_model=ClasseResponse, status_code=201, tags=["classes"])
def create_classe(
    body: ClasseCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur")),
):
    _get_or_404(db, AnneeScolaire, body.annee_scolaire_id, "Année scolaire")
    classe = Classe(name=body.name, annee_scolaire_id=body.annee_scolaire_id)
    db.add(classe)
    db.commit()
    db.refresh(classe)
    resp = ClasseResponse.model_validate(classe)
    resp.effectif = 0
    return resp


@app.get("/classes/{id}", response_model=ClasseResponse, tags=["classes"])
def get_classe(id: UUID, db: Session = Depends(get_db), _=Depends(get_current_user)):
    c = _get_or_404(db, Classe, id, "Classe")
    resp = ClasseResponse.model_validate(c)
    resp.effectif = len(c.inscriptions)
    return resp


@app.put("/classes/{id}", response_model=ClasseResponse, tags=["classes"])
def update_classe(
    id: UUID,
    body: ClasseUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur")),
):
    c = _get_or_404(db, Classe, id, "Classe")
    if body.name is not None:
        c.name = body.name
    db.commit()
    db.refresh(c)
    resp = ClasseResponse.model_validate(c)
    resp.effectif = len(c.inscriptions)
    return resp


@app.delete("/classes/{id}", status_code=204, tags=["classes"])
def delete_classe(
    id: UUID, db: Session = Depends(get_db), _=Depends(require_roles("administrateur"))
):
    c = _get_or_404(db, Classe, id, "Classe")
    if c.inscriptions:
        raise HTTPException(
            status_code=409,
            detail="Impossible de supprimer une classe avec des élèves inscrits",
        )
    db.delete(c)
    db.commit()


@app.get("/classes/{id}/eleves", response_model=List[EleveResponse], tags=["classes"])
def get_eleves_classe(
    id: UUID, db: Session = Depends(get_db), _=Depends(get_current_user)
):
    c = _get_or_404(db, Classe, id, "Classe")
    eleve_ids = [i.eleve_id for i in c.inscriptions]
    return db.query(Eleve).filter(Eleve.id.in_(eleve_ids)).all()


@app.get(
    "/classes/{id}/formateurs", response_model=List[FormateurResponse], tags=["classes"]
)
def get_formateurs_classe(
    id: UUID,
    annee_scolaire_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    c = _get_or_404(db, Classe, id, "Classe")
    q = db.query(Formateur).join(
        formateur_classe,
        and_(
            formateur_classe.c.formateur_id == Formateur.id,
            formateur_classe.c.classe_id == id,
        ),
    )
    if annee_scolaire_id:
        q = q.filter(formateur_classe.c.annee_scolaire_id == annee_scolaire_id)
    return q.all()


# ===========================================================================
# MATIÈRES
# ===========================================================================


@app.get("/matieres/", response_model=List[MatiereResponse], tags=["matieres"])
def list_matieres(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Matiere).order_by(Matiere.name).all()


@app.post(
    "/matieres/", response_model=MatiereResponse, status_code=201, tags=["matieres"]
)
def create_matiere(
    body: MatiereCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur", "responsable_pedagogique")),
):
    if db.query(Matiere).filter(Matiere.name == body.name).first():
        raise HTTPException(status_code=409, detail="Matière déjà existante")
    m = Matiere(name=body.name)
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


@app.get("/matieres/{id}", response_model=MatiereResponse, tags=["matieres"])
def get_matiere(id: UUID, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return _get_or_404(db, Matiere, id, "Matière")


@app.put("/matieres/{id}", response_model=MatiereResponse, tags=["matieres"])
def update_matiere(
    id: UUID,
    body: MatiereUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur", "responsable_pedagogique")),
):
    m = _get_or_404(db, Matiere, id, "Matière")
    if body.name is not None:
        m.name = body.name
    db.commit()
    db.refresh(m)
    return m


@app.delete("/matieres/{id}", status_code=204, tags=["matieres"])
def delete_matiere(
    id: UUID, db: Session = Depends(get_db), _=Depends(require_roles("administrateur"))
):
    m = _get_or_404(db, Matiere, id, "Matière")
    db.delete(m)
    db.commit()


# ===========================================================================
# FORMATEURS  (profils permanents)
# ===========================================================================


@app.get("/formateurs/", response_model=List[FormateurResponse], tags=["formateurs"])
def list_formateurs(
    annee_scolaire_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    if annee_scolaire_id:
        # Formateurs ayant au moins une attribution pour cette année
        fmt_ids = (
            db.execute(
                formateur_classe.select()
                .where(formateur_classe.c.annee_scolaire_id == annee_scolaire_id)
                .with_only_columns(formateur_classe.c.formateur_id)
                .distinct()
            )
            .scalars()
            .all()
        )
        return db.query(Formateur).filter(Formateur.id.in_(fmt_ids)).all()
    return db.query(Formateur).all()


@app.post(
    "/formateurs/",
    response_model=FormateurResponse,
    status_code=201,
    tags=["formateurs"],
)
def create_formateur(
    body: FormateurCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur")),
):
    user = _create_utilisateur(db, body.name, body.firstname, body.email, body.password)
    fmt = Formateur(user_id=user.id)
    db.add(fmt)
    db.commit()
    db.refresh(fmt)
    return fmt


@app.get("/formateurs/{id}", response_model=FormateurResponse, tags=["formateurs"])
def get_formateur(id: UUID, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return _get_or_404(db, Formateur, id, "Formateur")


@app.delete("/formateurs/{id}", status_code=204, tags=["formateurs"])
def delete_formateur(
    id: UUID, db: Session = Depends(get_db), _=Depends(require_roles("administrateur"))
):
    fmt = _get_or_404(db, Formateur, id, "Formateur")
    db.delete(fmt)
    db.commit()


@app.post("/formateurs/{id}/matieres", status_code=204, tags=["formateurs"])
def attribuer_matiere(
    id: UUID,
    body: FormateurAttribuerMatiere,
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur", "responsable_pedagogique")),
):
    _get_or_404(db, Formateur, id, "Formateur")
    _get_or_404(db, Matiere, body.matiere_id, "Matière")
    _get_or_404(db, AnneeScolaire, body.annee_scolaire_id, "Année scolaire")
    existing = db.execute(
        formateur_matiere.select().where(
            and_(
                formateur_matiere.c.formateur_id == id,
                formateur_matiere.c.matiere_id == body.matiere_id,
                formateur_matiere.c.annee_scolaire_id == body.annee_scolaire_id,
            )
        )
    ).first()
    if not existing:
        db.execute(
            formateur_matiere.insert().values(
                formateur_id=id,
                matiere_id=body.matiere_id,
                annee_scolaire_id=body.annee_scolaire_id,
            )
        )
        db.commit()


@app.delete(
    "/formateurs/{id}/matieres/{matiere_id}", status_code=204, tags=["formateurs"]
)
def retirer_matiere(
    id: UUID,
    matiere_id: UUID,
    annee_scolaire_id: UUID,
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur", "responsable_pedagogique")),
):
    db.execute(
        formateur_matiere.delete().where(
            and_(
                formateur_matiere.c.formateur_id == id,
                formateur_matiere.c.matiere_id == matiere_id,
                formateur_matiere.c.annee_scolaire_id == annee_scolaire_id,
            )
        )
    )
    db.commit()


@app.post("/formateurs/{id}/classes", status_code=204, tags=["formateurs"])
def attribuer_classe(
    id: UUID,
    body: FormateurAttribuerClasse,
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur", "responsable_pedagogique")),
):
    _get_or_404(db, Formateur, id, "Formateur")
    _get_or_404(db, Classe, body.classe_id, "Classe")
    _get_or_404(db, AnneeScolaire, body.annee_scolaire_id, "Année scolaire")
    existing = db.execute(
        formateur_classe.select().where(
            and_(
                formateur_classe.c.formateur_id == id,
                formateur_classe.c.classe_id == body.classe_id,
                formateur_classe.c.annee_scolaire_id == body.annee_scolaire_id,
            )
        )
    ).first()
    if not existing:
        db.execute(
            formateur_classe.insert().values(
                formateur_id=id,
                classe_id=body.classe_id,
                annee_scolaire_id=body.annee_scolaire_id,
            )
        )
        db.commit()


@app.delete(
    "/formateurs/{id}/classes/{classe_id}", status_code=204, tags=["formateurs"]
)
def retirer_classe(
    id: UUID,
    classe_id: UUID,
    annee_scolaire_id: UUID,
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur", "responsable_pedagogique")),
):
    db.execute(
        formateur_classe.delete().where(
            and_(
                formateur_classe.c.formateur_id == id,
                formateur_classe.c.classe_id == classe_id,
                formateur_classe.c.annee_scolaire_id == annee_scolaire_id,
            )
        )
    )
    db.commit()


@app.get("/formateurs/{id}/attributions", tags=["formateurs"])
def get_attributions(
    id: UUID,
    annee_scolaire_id: UUID,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    fmt = _get_or_404(db, Formateur, id, "Formateur")
    matieres = (
        db.query(Matiere)
        .join(
            formateur_matiere,
            and_(
                formateur_matiere.c.matiere_id == Matiere.id,
                formateur_matiere.c.formateur_id == id,
                formateur_matiere.c.annee_scolaire_id == annee_scolaire_id,
            ),
        )
        .all()
    )
    classes = (
        db.query(Classe)
        .join(
            formateur_classe,
            and_(
                formateur_classe.c.classe_id == Classe.id,
                formateur_classe.c.formateur_id == id,
                formateur_classe.c.annee_scolaire_id == annee_scolaire_id,
            ),
        )
        .all()
    )
    return {
        "formateur_id": id,
        "annee_scolaire_id": annee_scolaire_id,
        "matieres": [MatiereResponse.model_validate(m) for m in matieres],
        "classes": [ClasseResponse.model_validate(c) for c in classes],
    }


# ===========================================================================
# PARENTS
# ===========================================================================


@app.get("/parents/", response_model=List[ParentResponse], tags=["parents"])
def list_parents(
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur", "directeur")),
):
    return db.query(Parent).all()


@app.post("/parents/", response_model=ParentResponse, status_code=201, tags=["parents"])
def create_parent(
    body: ParentCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur")),
):
    user = _create_utilisateur(db, body.name, body.firstname, body.email, body.password)
    parent = Parent(user_id=user.id)
    db.add(parent)
    db.flush()
    for eid in body.eleve_ids:
        eleve = _get_or_404(db, Eleve, eid, "Élève")
        parent.eleves.append(eleve)
    db.commit()
    db.refresh(parent)
    return parent


@app.get("/parents/{id}", response_model=ParentResponse, tags=["parents"])
def get_parent(id: UUID, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return _get_or_404(db, Parent, id, "Parent")


@app.put("/parents/{id}", response_model=ParentResponse, tags=["parents"])
def update_parent(
    id: UUID,
    body: ParentUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur")),
):
    parent = _get_or_404(db, Parent, id, "Parent")
    if body.eleve_ids is not None:
        parent.eleves = [_get_or_404(db, Eleve, eid, "Élève") for eid in body.eleve_ids]
    db.commit()
    db.refresh(parent)
    return parent


@app.delete("/parents/{id}", status_code=204, tags=["parents"])
def delete_parent(
    id: UUID, db: Session = Depends(get_db), _=Depends(require_roles("administrateur"))
):
    parent = _get_or_404(db, Parent, id, "Parent")
    db.delete(parent)
    db.commit()


# ===========================================================================
# RÔLES : Directeur / Administrateur / ResponsablePedagogique
# ===========================================================================


def _create_role(model_class, db: Session, body: RoleCreate):
    user = _create_utilisateur(db, body.name, body.firstname, body.email, body.password)
    obj = model_class(user_id=user.id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/directeurs/", response_model=List[RoleResponse], tags=["roles"])
def list_directeurs(
    db: Session = Depends(get_db), _=Depends(require_roles("administrateur"))
):
    return db.query(Directeur).all()


@app.post("/directeurs/", response_model=RoleResponse, status_code=201, tags=["roles"])
def create_directeur(
    body: RoleCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur")),
):
    return _create_role(Directeur, db, body)


@app.delete("/directeurs/{id}", status_code=204, tags=["roles"])
def delete_directeur(
    id: UUID, db: Session = Depends(get_db), _=Depends(require_roles("administrateur"))
):
    obj = _get_or_404(db, Directeur, id, "Directeur")
    db.delete(obj)
    db.commit()


@app.get("/administrateurs/", response_model=List[RoleResponse], tags=["roles"])
def list_administrateurs(
    db: Session = Depends(get_db), _=Depends(require_roles("administrateur"))
):
    return db.query(Administrateur).all()


@app.post(
    "/administrateurs/", response_model=RoleResponse, status_code=201, tags=["roles"]
)
def create_administrateur(
    body: RoleCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur")),
):
    return _create_role(Administrateur, db, body)


@app.delete("/administrateurs/{id}", status_code=204, tags=["roles"])
def delete_administrateur(
    id: UUID, db: Session = Depends(get_db), _=Depends(require_roles("administrateur"))
):
    obj = _get_or_404(db, Administrateur, id, "Administrateur")
    db.delete(obj)
    db.commit()


@app.get(
    "/responsables-pedagogiques/", response_model=List[RoleResponse], tags=["roles"]
)
def list_responsables(
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur", "directeur")),
):
    return db.query(ResponsablePedagogique).all()


@app.post(
    "/responsables-pedagogiques/",
    response_model=RoleResponse,
    status_code=201,
    tags=["roles"],
)
def create_responsable(
    body: RoleCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur")),
):
    return _create_role(ResponsablePedagogique, db, body)


@app.delete("/responsables-pedagogiques/{id}", status_code=204, tags=["roles"])
def delete_responsable(
    id: UUID, db: Session = Depends(get_db), _=Depends(require_roles("administrateur"))
):
    obj = _get_or_404(db, ResponsablePedagogique, id, "Responsable pédagogique")
    db.delete(obj)
    db.commit()


# ===========================================================================
# COURS
# ===========================================================================


@app.get("/cours/", response_model=List[CoursResponse], tags=["cours"])
def list_cours(
    annee_scolaire_id: Optional[UUID] = None,
    classe_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    q = db.query(Cours)
    if classe_id:
        q = q.filter(Cours.classe_id == classe_id)
    if annee_scolaire_id:
        q = q.join(Classe).filter(Classe.annee_scolaire_id == annee_scolaire_id)
    return q.all()


@app.post("/cours/", response_model=CoursResponse, status_code=201, tags=["cours"])
def create_cours(
    body: CoursCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("formateur", "administrateur")),
):
    cours = Cours(**body.model_dump(), created_at=datetime.now(timezone.utc))
    db.add(cours)
    db.commit()
    db.refresh(cours)
    return cours


@app.get("/cours/{id}", response_model=CoursResponse, tags=["cours"])
def get_cours(id: UUID, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return _get_or_404(db, Cours, id, "Cours")


@app.put("/cours/{id}", response_model=CoursResponse, tags=["cours"])
def update_cours(
    id: UUID,
    body: CoursUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("formateur", "administrateur")),
):
    cours = _get_or_404(db, Cours, id, "Cours")
    if body.titre is not None:
        cours.titre = body.titre
    if body.description is not None:
        cours.description = body.description
    db.commit()
    db.refresh(cours)
    return cours


@app.delete("/cours/{id}", status_code=204, tags=["cours"])
def delete_cours(
    id: UUID,
    db: Session = Depends(get_db),
    _=Depends(require_roles("formateur", "administrateur")),
):
    cours = _get_or_404(db, Cours, id, "Cours")
    db.delete(cours)
    db.commit()


@app.post(
    "/cours/{id}/supports",
    response_model=SupportPedagogiqueResponse,
    status_code=201,
    tags=["cours"],
)
def add_support(
    id: UUID,
    body: SupportPedagogiqueCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("formateur", "administrateur")),
):
    _get_or_404(db, Cours, id, "Cours")
    support = SupportPedagogique(
        cours_id=id, nom=body.nom, url=body.url, type=body.type
    )
    db.add(support)
    db.commit()
    db.refresh(support)
    return support


@app.delete("/cours/{cours_id}/supports/{support_id}", status_code=204, tags=["cours"])
def delete_support(
    cours_id: UUID,
    support_id: UUID,
    db: Session = Depends(get_db),
    _=Depends(require_roles("formateur", "administrateur")),
):
    support = _get_or_404(db, SupportPedagogique, support_id, "Support")
    if support.cours_id != cours_id:
        raise HTTPException(status_code=404, detail="Support introuvable dans ce cours")
    db.delete(support)
    db.commit()


# ===========================================================================
# DEVOIRS
# ===========================================================================


@app.get("/devoirs/", response_model=List[DevoirResponse], tags=["devoirs"])
def list_devoirs(
    annee_scolaire_id: Optional[UUID] = None,
    classe_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    q = db.query(Devoir)
    if classe_id:
        q = q.filter(Devoir.classe_id == classe_id)
    if annee_scolaire_id:
        q = q.join(Classe).filter(Classe.annee_scolaire_id == annee_scolaire_id)
    return q.all()


@app.post("/devoirs/", response_model=DevoirResponse, status_code=201, tags=["devoirs"])
def create_devoir(
    body: DevoirCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("formateur", "administrateur")),
):
    devoir = Devoir(**body.model_dump(), created_at=datetime.now(timezone.utc))
    db.add(devoir)
    db.commit()
    db.refresh(devoir)
    return devoir


@app.get("/devoirs/{id}", response_model=DevoirResponse, tags=["devoirs"])
def get_devoir(id: UUID, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return _get_or_404(db, Devoir, id, "Devoir")


@app.put("/devoirs/{id}", response_model=DevoirResponse, tags=["devoirs"])
def update_devoir(
    id: UUID,
    body: DevoirUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("formateur", "administrateur")),
):
    devoir = _get_or_404(db, Devoir, id, "Devoir")
    if body.titre is not None:
        devoir.titre = body.titre
    if body.consigne is not None:
        devoir.consigne = body.consigne
    if body.date_limite is not None:
        devoir.date_limite = body.date_limite
    db.commit()
    db.refresh(devoir)
    return devoir


@app.delete("/devoirs/{id}", status_code=204, tags=["devoirs"])
def delete_devoir(
    id: UUID,
    db: Session = Depends(get_db),
    _=Depends(require_roles("formateur", "administrateur")),
):
    devoir = _get_or_404(db, Devoir, id, "Devoir")
    db.delete(devoir)
    db.commit()


@app.post(
    "/devoirs/{id}/soumettre",
    response_model=SoumissionResponse,
    status_code=201,
    tags=["devoirs"],
)
def soumettre(
    id: UUID,
    body: SoumissionCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _get_or_404(db, Devoir, id, "Devoir")
    soumission = Soumission(
        devoir_id=id,
        eleve_id=body.eleve_id,
        contenu=body.contenu,
        soumis_le=datetime.now(timezone.utc),
    )
    db.add(soumission)
    db.commit()
    db.refresh(soumission)
    return soumission


@app.put(
    "/devoirs/{id}/soumissions/{eleve_id}/corriger",
    response_model=SoumissionResponse,
    tags=["devoirs"],
)
def corriger(
    id: UUID,
    eleve_id: UUID,
    body: SoumissionCorriger,
    db: Session = Depends(get_db),
    _=Depends(require_roles("formateur", "administrateur")),
):
    soumission = (
        db.query(Soumission)
        .filter(Soumission.devoir_id == id, Soumission.eleve_id == eleve_id)
        .first()
    )
    if not soumission:
        raise HTTPException(status_code=404, detail="Soumission introuvable")
    if body.note is not None:
        soumission.note = body.note
    if body.appreciation is not None:
        soumission.appreciation = body.appreciation
    soumission.corrige_le = datetime.now(timezone.utc)
    db.commit()
    db.refresh(soumission)
    return soumission


# ===========================================================================
# ÉVALUATIONS
# ===========================================================================


@app.get("/evaluations/", response_model=List[EvaluationResponse], tags=["evaluations"])
def list_evaluations(
    annee_scolaire_id: Optional[UUID] = None,
    classe_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    q = db.query(Evaluation)
    if annee_scolaire_id:
        q = q.filter(Evaluation.annee_scolaire_id == annee_scolaire_id)
    if classe_id:
        q = q.filter(Evaluation.classe_id == classe_id)
    return q.all()


@app.post(
    "/evaluations/",
    response_model=EvaluationResponse,
    status_code=201,
    tags=["evaluations"],
)
def create_evaluation(
    body: EvaluationCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("formateur", "administrateur", "responsable_pedagogique")),
):
    ev = Evaluation(**body.model_dump())
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return ev


@app.get("/evaluations/{id}", response_model=EvaluationResponse, tags=["evaluations"])
def get_evaluation(
    id: UUID, db: Session = Depends(get_db), _=Depends(get_current_user)
):
    return _get_or_404(db, Evaluation, id, "Évaluation")


@app.put("/evaluations/{id}", response_model=EvaluationResponse, tags=["evaluations"])
def update_evaluation(
    id: UUID,
    body: EvaluationUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("formateur", "administrateur")),
):
    ev = _get_or_404(db, Evaluation, id, "Évaluation")
    if body.titre is not None:
        ev.titre = body.titre
    if body.date is not None:
        ev.date = body.date
    if body.bareme is not None:
        ev.bareme = body.bareme
    db.commit()
    db.refresh(ev)
    return ev


@app.delete("/evaluations/{id}", status_code=204, tags=["evaluations"])
def delete_evaluation(
    id: UUID, db: Session = Depends(get_db), _=Depends(require_roles("administrateur"))
):
    ev = _get_or_404(db, Evaluation, id, "Évaluation")
    db.delete(ev)
    db.commit()


@app.post(
    "/evaluations/{id}/notes",
    response_model=List[NoteResponse],
    status_code=201,
    tags=["evaluations"],
)
def batch_notes(
    id: UUID,
    body: NoteBatch,
    db: Session = Depends(get_db),
    _=Depends(require_roles("formateur", "administrateur")),
):
    _get_or_404(db, Evaluation, id, "Évaluation")
    created = []
    for n in body.notes:
        existing = (
            db.query(Note)
            .filter(Note.eleve_id == n.eleve_id, Note.evaluation_id == id)
            .first()
        )
        if existing:
            existing.valeur = n.valeur
            existing.commentaire = n.commentaire
            db.flush()
            created.append(existing)
        else:
            note = Note(
                eleve_id=n.eleve_id,
                evaluation_id=id,
                valeur=n.valeur,
                commentaire=n.commentaire,
            )
            db.add(note)
            db.flush()
            created.append(note)
    db.commit()
    return created


@app.put(
    "/evaluations/{id}/notes/{eleve_id}",
    response_model=NoteResponse,
    tags=["evaluations"],
)
def update_note(
    id: UUID,
    eleve_id: UUID,
    body: NoteUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("formateur", "administrateur")),
):
    note = (
        db.query(Note)
        .filter(Note.evaluation_id == id, Note.eleve_id == eleve_id)
        .first()
    )
    if not note:
        raise HTTPException(status_code=404, detail="Note introuvable")
    if body.valeur is not None:
        note.valeur = body.valeur
    if body.commentaire is not None:
        note.commentaire = body.commentaire
    db.commit()
    db.refresh(note)
    return note


# ===========================================================================
# ABSENCES
# ===========================================================================


@app.get("/absences/", response_model=List[AbsenceResponse], tags=["absences"])
def list_absences(
    eleve_id: Optional[UUID] = None,
    classe_id: Optional[UUID] = None,
    annee_scolaire_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    q = db.query(Absence)
    if eleve_id:
        q = q.filter(Absence.eleve_id == eleve_id)
    if classe_id:
        q = q.filter(Absence.classe_id == classe_id)
    if annee_scolaire_id:
        q = q.filter(Absence.annee_scolaire_id == annee_scolaire_id)
    return q.all()


@app.post(
    "/absences/", response_model=AbsenceResponse, status_code=201, tags=["absences"]
)
def create_absence(
    body: AbsenceCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("formateur", "administrateur")),
):
    absence = Absence(**body.model_dump())
    db.add(absence)
    db.commit()
    db.refresh(absence)
    return absence


@app.put("/absences/{id}", response_model=AbsenceResponse, tags=["absences"])
def update_absence(
    id: UUID,
    body: AbsenceUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("formateur", "administrateur")),
):
    absence = _get_or_404(db, Absence, id, "Absence")
    if body.justifiee is not None:
        absence.justifiee = body.justifiee
    if body.motif is not None:
        absence.motif = body.motif
    db.commit()
    db.refresh(absence)
    return absence


@app.delete("/absences/{id}", status_code=204, tags=["absences"])
def delete_absence(
    id: UUID,
    db: Session = Depends(get_db),
    _=Depends(require_roles("formateur", "administrateur")),
):
    absence = _get_or_404(db, Absence, id, "Absence")
    db.delete(absence)
    db.commit()


# ===========================================================================
# EMPLOIS DU TEMPS
# ===========================================================================


@app.get(
    "/emplois-du-temps/",
    response_model=List[EmploiDuTempsResponse],
    tags=["emplois-du-temps"],
)
def list_edt(
    classe_id: Optional[UUID] = None,
    formateur_id: Optional[UUID] = None,
    annee_scolaire_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    q = db.query(EmploiDuTemps)
    if classe_id:
        q = q.filter(EmploiDuTemps.classe_id == classe_id)
    if formateur_id:
        q = q.filter(EmploiDuTemps.formateur_id == formateur_id)
    if annee_scolaire_id:
        q = q.filter(EmploiDuTemps.annee_scolaire_id == annee_scolaire_id)
    return q.all()


@app.post(
    "/emplois-du-temps/",
    response_model=EmploiDuTempsResponse,
    status_code=201,
    tags=["emplois-du-temps"],
)
def create_edt(
    body: EmploiDuTempsCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur", "responsable_pedagogique")),
):
    edt = EmploiDuTemps(**body.model_dump())
    db.add(edt)
    db.commit()
    db.refresh(edt)
    return edt


@app.put(
    "/emplois-du-temps/{id}",
    response_model=EmploiDuTempsResponse,
    tags=["emplois-du-temps"],
)
def update_edt(
    id: UUID,
    body: EmploiDuTempsUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur", "responsable_pedagogique")),
):
    edt = _get_or_404(db, EmploiDuTemps, id, "Créneau")
    if body.jour is not None:
        edt.jour = body.jour
    if body.heure_debut is not None:
        edt.heure_debut = body.heure_debut
    if body.heure_fin is not None:
        edt.heure_fin = body.heure_fin
    db.commit()
    db.refresh(edt)
    return edt


@app.delete("/emplois-du-temps/{id}", status_code=204, tags=["emplois-du-temps"])
def delete_edt(
    id: UUID,
    db: Session = Depends(get_db),
    _=Depends(require_roles("administrateur", "responsable_pedagogique")),
):
    edt = _get_or_404(db, EmploiDuTemps, id, "Créneau")
    db.delete(edt)
    db.commit()


# ===========================================================================
# ANNONCES
# ===========================================================================


@app.get("/annonces/", response_model=List[AnnonceResponse], tags=["annonces"])
def list_annonces(
    db: Session = Depends(get_db), current_user: Utilisateur = Depends(get_current_user)
):
    from app.auth import get_role

    role = get_role(current_user)
    q = db.query(Annonce)
    if role not in ("administrateur", "directeur"):
        q = q.filter(Annonce.audience.in_(["tous", role + "s"]))
    return q.order_by(Annonce.created_at.desc()).all()


@app.post(
    "/annonces/", response_model=AnnonceResponse, status_code=201, tags=["annonces"]
)
def create_annonce(
    body: AnnonceCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    annonce = Annonce(
        titre=body.titre,
        contenu=body.contenu,
        audience=body.audience,
        auteur_id=current_user.id,
        created_at=datetime.now(timezone.utc),
    )
    db.add(annonce)
    db.commit()
    db.refresh(annonce)
    return annonce


@app.get("/annonces/{id}", response_model=AnnonceResponse, tags=["annonces"])
def get_annonce(id: UUID, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return _get_or_404(db, Annonce, id, "Annonce")


@app.put("/annonces/{id}", response_model=AnnonceResponse, tags=["annonces"])
def update_annonce(
    id: UUID,
    body: AnnonceUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    annonce = _get_or_404(db, Annonce, id, "Annonce")
    if body.titre is not None:
        annonce.titre = body.titre
    if body.contenu is not None:
        annonce.contenu = body.contenu
    if body.audience is not None:
        annonce.audience = body.audience
    db.commit()
    db.refresh(annonce)
    return annonce


@app.delete("/annonces/{id}", status_code=204, tags=["annonces"])
def delete_annonce(
    id: UUID, db: Session = Depends(get_db), _=Depends(get_current_user)
):
    annonce = _get_or_404(db, Annonce, id, "Annonce")
    db.delete(annonce)
    db.commit()


# ===========================================================================
# NOTIFICATIONS
# ===========================================================================


@app.get(
    "/notifications/", response_model=List[NotificationResponse], tags=["notifications"]
)
def list_notifications(
    db: Session = Depends(get_db), current_user: Utilisateur = Depends(get_current_user)
):
    return (
        db.query(Notification)
        .filter(Notification.user_id == current_user.id)
        .order_by(Notification.created_at.desc())
        .all()
    )


@app.patch(
    "/notifications/{id}/lire",
    response_model=NotificationResponse,
    tags=["notifications"],
)
def marquer_lue(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    notif = _get_or_404(db, Notification, id, "Notification")
    if notif.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Accès interdit")
    notif.lue = True
    db.commit()
    db.refresh(notif)
    return notif


@app.patch("/notifications/lire-tout", status_code=204, tags=["notifications"])
def marquer_tout_lu(
    db: Session = Depends(get_db), current_user: Utilisateur = Depends(get_current_user)
):
    db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.lue == False,
    ).update({Notification.lue: True})
    db.commit()
