from app.database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Boolean,
    Float,
    DateTime,
    UniqueConstraint,
    Table,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid


# ---------------------------------------------------------------------------
# Tables d'association (Many-to-Many avec annee_scolaire_id)
# ---------------------------------------------------------------------------

# Attributions annuelles formateur ↔ matière
formateur_matiere = Table(
    "formateur_matiere",
    Base.metadata,
    Column(
        "formateur_id",
        UUID(as_uuid=True),
        ForeignKey("formateurs.id"),
        primary_key=True,
    ),
    Column(
        "matiere_id", UUID(as_uuid=True), ForeignKey("matieres.id"), primary_key=True
    ),
    Column(
        "annee_scolaire_id",
        UUID(as_uuid=True),
        ForeignKey("annee_scolaires.id"),
        primary_key=True,
    ),
)

# Attributions annuelles formateur ↔ classe
formateur_classe = Table(
    "formateur_classe",
    Base.metadata,
    Column(
        "formateur_id",
        UUID(as_uuid=True),
        ForeignKey("formateurs.id"),
        primary_key=True,
    ),
    Column("classe_id", UUID(as_uuid=True), ForeignKey("classes.id"), primary_key=True),
    Column(
        "annee_scolaire_id",
        UUID(as_uuid=True),
        ForeignKey("annee_scolaires.id"),
        primary_key=True,
    ),
)

# Association parent ↔ élève (un parent peut avoir plusieurs élèves)
parent_eleve = Table(
    "parent_eleve",
    Base.metadata,
    Column("parent_id", UUID(as_uuid=True), ForeignKey("parents.id"), primary_key=True),
    Column("eleve_id", UUID(as_uuid=True), ForeignKey("eleves.id"), primary_key=True),
)


# ---------------------------------------------------------------------------
# AnneeScolaire
# ---------------------------------------------------------------------------


class AnneeScolaire(Base):
    __tablename__ = "annee_scolaires"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False, index=True)
    is_active = Column(Boolean, default=False, nullable=False)

    classes = relationship("Classe", back_populates="annee_scolaire")
    inscriptions = relationship("Inscription", back_populates="annee_scolaire")


# ---------------------------------------------------------------------------
# Utilisateur  (compte permanent – email/password)
# ---------------------------------------------------------------------------


class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False, index=True)
    firstname = Column(String, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(Text, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # Relations vers les profils de rôle
    eleve = relationship("Eleve", back_populates="user", uselist=False)
    formateur = relationship("Formateur", back_populates="user", uselist=False)
    parent = relationship("Parent", back_populates="user", uselist=False)
    directeur = relationship("Directeur", back_populates="user", uselist=False)
    administrateur = relationship(
        "Administrateur", back_populates="user", uselist=False
    )
    responsable_ped = relationship(
        "ResponsablePedagogique", back_populates="user", uselist=False
    )


# ---------------------------------------------------------------------------
# Eleve  (profil permanent – créé une seule fois)
# ---------------------------------------------------------------------------


class Eleve(Base):
    __tablename__ = "eleves"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("utilisateurs.id"), nullable=False, index=True
    )
    matricule = Column(String, unique=True, nullable=False, index=True)

    user = relationship("Utilisateur", back_populates="eleve")
    inscriptions = relationship("Inscription", back_populates="eleve")
    notes = relationship("Note", back_populates="eleve")
    soumissions = relationship("Soumission", back_populates="eleve")
    absences = relationship("Absence", back_populates="eleve")
    parents = relationship("Parent", secondary=parent_eleve, back_populates="eleves")


# ---------------------------------------------------------------------------
# Inscription  (pivot annuel : élève × classe × année)
# ---------------------------------------------------------------------------


class Inscription(Base):
    __tablename__ = "inscriptions"
    __table_args__ = (
        UniqueConstraint(
            "eleve_id", "annee_scolaire_id", name="uq_inscription_eleve_annee"
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    eleve_id = Column(
        UUID(as_uuid=True), ForeignKey("eleves.id"), nullable=False, index=True
    )
    classe_id = Column(
        UUID(as_uuid=True), ForeignKey("classes.id"), nullable=True, index=True
    )
    annee_scolaire_id = Column(
        UUID(as_uuid=True), ForeignKey("annee_scolaires.id"), nullable=False, index=True
    )
    is_ancien = Column(Boolean, default=False, nullable=False)
    date_inscription = Column(DateTime)

    eleve = relationship("Eleve", back_populates="inscriptions")
    classe = relationship("Classe", back_populates="inscriptions")
    annee_scolaire = relationship("AnneeScolaire", back_populates="inscriptions")


# ---------------------------------------------------------------------------
# Classe  (entité annuelle)
# ---------------------------------------------------------------------------


class Classe(Base):
    __tablename__ = "classes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False, index=True)
    annee_scolaire_id = Column(
        UUID(as_uuid=True), ForeignKey("annee_scolaires.id"), nullable=False, index=True
    )

    annee_scolaire = relationship("AnneeScolaire", back_populates="classes")
    inscriptions = relationship("Inscription", back_populates="classe")
    formateurs = relationship(
        "Formateur", secondary=formateur_classe, back_populates="classes"
    )
    cours = relationship("Cours", back_populates="classe")
    evaluations = relationship("Evaluation", back_populates="classe")
    devoirs = relationship("Devoir", back_populates="classe")
    absences = relationship("Absence", back_populates="classe")
    emplois_dt = relationship("EmploiDuTemps", back_populates="classe")


# ---------------------------------------------------------------------------
# Matiere  (entité permanente)
# ---------------------------------------------------------------------------


class Matiere(Base):
    __tablename__ = "matieres"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False, unique=True, index=True)

    formateurs = relationship(
        "Formateur", secondary=formateur_matiere, back_populates="matieres"
    )
    cours = relationship("Cours", back_populates="matiere")
    evaluations = relationship("Evaluation", back_populates="matiere")
    emplois_dt = relationship("EmploiDuTemps", back_populates="matiere")


# ---------------------------------------------------------------------------
# Formateur  (profil permanent)
# ---------------------------------------------------------------------------


class Formateur(Base):
    __tablename__ = "formateurs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("utilisateurs.id"), nullable=False, index=True
    )

    user = relationship("Utilisateur", back_populates="formateur")
    matieres = relationship(
        "Matiere", secondary=formateur_matiere, back_populates="formateurs"
    )
    classes = relationship(
        "Classe", secondary=formateur_classe, back_populates="formateurs"
    )
    cours = relationship("Cours", back_populates="formateur")
    devoirs = relationship("Devoir", back_populates="formateur")
    absences = relationship("Absence", back_populates="formateur")
    emplois_dt = relationship("EmploiDuTemps", back_populates="formateur")


# ---------------------------------------------------------------------------
# Parent
# ---------------------------------------------------------------------------


class Parent(Base):
    __tablename__ = "parents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("utilisateurs.id"), nullable=False, index=True
    )

    user = relationship("Utilisateur", back_populates="parent")
    eleves = relationship("Eleve", secondary=parent_eleve, back_populates="parents")


# ---------------------------------------------------------------------------
# Directeur / Administrateur / ResponsablePedagogique
# ---------------------------------------------------------------------------


class Directeur(Base):
    __tablename__ = "directeurs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("utilisateurs.id"), nullable=False, index=True
    )

    user = relationship("Utilisateur", back_populates="directeur")


class Administrateur(Base):
    __tablename__ = "administrateurs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("utilisateurs.id"), nullable=False, index=True
    )

    user = relationship("Utilisateur", back_populates="administrateur")


class ResponsablePedagogique(Base):
    __tablename__ = "responsables_pedagogiques"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("utilisateurs.id"), nullable=False, index=True
    )

    user = relationship("Utilisateur", back_populates="responsable_ped")


# ---------------------------------------------------------------------------
# Cours  (annuel via classe)
# ---------------------------------------------------------------------------


class Cours(Base):
    __tablename__ = "cours"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    titre = Column(String, nullable=False)
    description = Column(Text)
    formateur_id = Column(
        UUID(as_uuid=True), ForeignKey("formateurs.id"), nullable=False, index=True
    )
    matiere_id = Column(
        UUID(as_uuid=True), ForeignKey("matieres.id"), nullable=False, index=True
    )
    classe_id = Column(
        UUID(as_uuid=True), ForeignKey("classes.id"), nullable=False, index=True
    )
    created_at = Column(DateTime)

    formateur = relationship("Formateur", back_populates="cours")
    matiere = relationship("Matiere", back_populates="cours")
    classe = relationship("Classe", back_populates="cours")
    supports = relationship(
        "SupportPedagogique", back_populates="cours", cascade="all, delete-orphan"
    )
    devoirs = relationship("Devoir", back_populates="cours")


# ---------------------------------------------------------------------------
# SupportPedagogique
# ---------------------------------------------------------------------------


class SupportPedagogique(Base):
    __tablename__ = "supports_pedagogiques"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    cours_id = Column(
        UUID(as_uuid=True), ForeignKey("cours.id"), nullable=False, index=True
    )
    nom = Column(String, nullable=False)
    url = Column(String, nullable=False)
    type = Column(String)  # "pdf", "video", "image", etc.

    cours = relationship("Cours", back_populates="supports")


# ---------------------------------------------------------------------------
# Devoir
# ---------------------------------------------------------------------------


class Devoir(Base):
    __tablename__ = "devoirs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    titre = Column(String, nullable=False)
    consigne = Column(Text)
    cours_id = Column(
        UUID(as_uuid=True), ForeignKey("cours.id"), nullable=True, index=True
    )
    classe_id = Column(
        UUID(as_uuid=True), ForeignKey("classes.id"), nullable=False, index=True
    )
    formateur_id = Column(
        UUID(as_uuid=True), ForeignKey("formateurs.id"), nullable=False, index=True
    )
    date_limite = Column(DateTime)
    created_at = Column(DateTime)

    cours = relationship("Cours", back_populates="devoirs")
    classe = relationship("Classe", back_populates="devoirs")
    formateur = relationship("Formateur", back_populates="devoirs")
    soumissions = relationship(
        "Soumission", back_populates="devoir", cascade="all, delete-orphan"
    )


# ---------------------------------------------------------------------------
# Soumission
# ---------------------------------------------------------------------------


class Soumission(Base):
    __tablename__ = "soumissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    devoir_id = Column(
        UUID(as_uuid=True), ForeignKey("devoirs.id"), nullable=False, index=True
    )
    eleve_id = Column(
        UUID(as_uuid=True), ForeignKey("eleves.id"), nullable=False, index=True
    )
    contenu = Column(Text)
    note = Column(Float)
    appreciation = Column(Text)
    soumis_le = Column(DateTime)
    corrige_le = Column(DateTime)

    devoir = relationship("Devoir", back_populates="soumissions")
    eleve = relationship("Eleve", back_populates="soumissions")


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    titre = Column(String, nullable=False)
    matiere_id = Column(
        UUID(as_uuid=True), ForeignKey("matieres.id"), nullable=False, index=True
    )
    classe_id = Column(
        UUID(as_uuid=True), ForeignKey("classes.id"), nullable=False, index=True
    )
    annee_scolaire_id = Column(
        UUID(as_uuid=True), ForeignKey("annee_scolaires.id"), nullable=False, index=True
    )
    date = Column(DateTime)
    bareme = Column(Integer, default=20)

    matiere = relationship("Matiere", back_populates="evaluations")
    classe = relationship("Classe", back_populates="evaluations")
    notes = relationship(
        "Note", back_populates="evaluation", cascade="all, delete-orphan"
    )


# ---------------------------------------------------------------------------
# Note
# ---------------------------------------------------------------------------


class Note(Base):
    __tablename__ = "notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    eleve_id = Column(
        UUID(as_uuid=True), ForeignKey("eleves.id"), nullable=False, index=True
    )
    evaluation_id = Column(
        UUID(as_uuid=True), ForeignKey("evaluations.id"), nullable=False, index=True
    )
    valeur = Column(Float, nullable=False)
    commentaire = Column(Text)

    eleve = relationship("Eleve", back_populates="notes")
    evaluation = relationship("Evaluation", back_populates="notes")


# ---------------------------------------------------------------------------
# Absence
# ---------------------------------------------------------------------------


class Absence(Base):
    __tablename__ = "absences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    eleve_id = Column(
        UUID(as_uuid=True), ForeignKey("eleves.id"), nullable=False, index=True
    )
    formateur_id = Column(
        UUID(as_uuid=True), ForeignKey("formateurs.id"), nullable=False, index=True
    )
    classe_id = Column(
        UUID(as_uuid=True), ForeignKey("classes.id"), nullable=False, index=True
    )
    annee_scolaire_id = Column(
        UUID(as_uuid=True), ForeignKey("annee_scolaires.id"), nullable=False, index=True
    )
    date = Column(DateTime, nullable=False)
    justifiee = Column(Boolean, default=False)
    motif = Column(Text)

    eleve = relationship("Eleve", back_populates="absences")
    formateur = relationship("Formateur", back_populates="absences")
    classe = relationship("Classe", back_populates="absences")


# ---------------------------------------------------------------------------
# EmploiDuTemps
# ---------------------------------------------------------------------------


class EmploiDuTemps(Base):
    __tablename__ = "emplois_du_temps"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    classe_id = Column(
        UUID(as_uuid=True), ForeignKey("classes.id"), nullable=False, index=True
    )
    formateur_id = Column(
        UUID(as_uuid=True), ForeignKey("formateurs.id"), nullable=False, index=True
    )
    matiere_id = Column(
        UUID(as_uuid=True), ForeignKey("matieres.id"), nullable=False, index=True
    )
    annee_scolaire_id = Column(
        UUID(as_uuid=True), ForeignKey("annee_scolaires.id"), nullable=False, index=True
    )
    jour = Column(String, nullable=False)  # "Lundi", "Mardi", etc.
    heure_debut = Column(String, nullable=False)  # "08:00"
    heure_fin = Column(String, nullable=False)  # "10:00"

    classe = relationship("Classe", back_populates="emplois_dt")
    formateur = relationship("Formateur", back_populates="emplois_dt")
    matiere = relationship("Matiere", back_populates="emplois_dt")


# ---------------------------------------------------------------------------
# Annonce
# ---------------------------------------------------------------------------


class Annonce(Base):
    __tablename__ = "annonces"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    titre = Column(String, nullable=False)
    contenu = Column(Text, nullable=False)
    auteur_id = Column(
        UUID(as_uuid=True), ForeignKey("utilisateurs.id"), nullable=False, index=True
    )
    audience = Column(
        String, default="tous"
    )  # "tous", "eleves", "parents", "formateurs"
    created_at = Column(DateTime)


# ---------------------------------------------------------------------------
# Notification
# ---------------------------------------------------------------------------


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("utilisateurs.id"), nullable=False, index=True
    )
    message = Column(Text, nullable=False)
    lue = Column(Boolean, default=False)
    created_at = Column(DateTime)
