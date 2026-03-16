from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict, field_validator


# ===========================================================================
# Helpers
# ===========================================================================


class OrmBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ===========================================================================
# Auth
# ===========================================================================


class UtilisateurLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ===========================================================================
# AnneeScolaire
# ===========================================================================


class AnneeScolaireBase(BaseModel):
    name: str


class AnneeScolaireCreate(AnneeScolaireBase):
    pass


class AnneeScolaireResponse(OrmBase, AnneeScolaireBase):
    id: UUID
    is_active: bool


# ===========================================================================
# Utilisateur
# ===========================================================================


class UtilisateurBase(BaseModel):
    name: str
    firstname: str
    email: EmailStr


class UtilisateurCreate(UtilisateurBase):
    password: str


class UtilisateurUpdate(BaseModel):
    name: Optional[str] = None
    firstname: Optional[str] = None
    email: Optional[EmailStr] = None


class UtilisateurResetPassword(BaseModel):
    new_password: str


class UtilisateurResponse(OrmBase, UtilisateurBase):
    id: UUID
    created_at: Optional[datetime] = None


# ===========================================================================
# Eleve  (profil permanent)
# ===========================================================================


class EleveBase(BaseModel):
    matricule: str


class EleveCreate(EleveBase):
    """Crée le profil élève + le compte utilisateur associé."""

    name: str
    firstname: str
    email: EmailStr
    password: str


class EleveUpdate(BaseModel):
    matricule: Optional[str] = None


class EleveResponse(OrmBase, EleveBase):
    id: UUID
    user: UtilisateurResponse


# ===========================================================================
# Inscription  (pivot annuel)
# ===========================================================================


class InscriptionBase(BaseModel):
    eleve_id: UUID
    annee_scolaire_id: UUID
    classe_id: Optional[UUID] = None
    is_ancien: bool = False


class InscriptionCreate(InscriptionBase):
    pass


class InscriptionReinscription(BaseModel):
    """Réinscrire un élève depuis une année passée dans la nouvelle année active."""

    eleve_id: UUID
    annee_scolaire_id: UUID  # nouvelle année cible
    classe_id: Optional[UUID] = None


class InscriptionUpdate(BaseModel):
    classe_id: Optional[UUID] = None


class InscriptionResponse(OrmBase, InscriptionBase):
    id: UUID
    date_inscription: Optional[datetime] = None
    eleve: EleveResponse


# ===========================================================================
# Matiere
# ===========================================================================


class MatiereBase(BaseModel):
    name: str


class MatiereCreate(MatiereBase):
    pass


class MatiereUpdate(BaseModel):
    name: Optional[str] = None


class MatiereResponse(OrmBase, MatiereBase):
    id: UUID


# ===========================================================================
# Classe
# ===========================================================================


class ClasseBase(BaseModel):
    name: str
    annee_scolaire_id: UUID


class ClasseCreate(ClasseBase):
    pass


class ClasseUpdate(BaseModel):
    name: Optional[str] = None


class ClasseResponse(OrmBase, ClasseBase):
    id: UUID
    effectif: Optional[int] = None  # calculé côté route


# ===========================================================================
# Formateur  (profil permanent)
# ===========================================================================


class FormateurBase(BaseModel):
    pass  # les données personnelles sont dans Utilisateur


class FormateurCreate(BaseModel):
    """Crée le profil formateur + le compte utilisateur associé."""

    name: str
    firstname: str
    email: EmailStr
    password: str


class FormateurUpdate(BaseModel):
    pass


class FormateurResponse(OrmBase):
    id: UUID
    user: UtilisateurResponse
    matieres: List[MatiereResponse] = []
    classes: List[ClasseResponse] = []


class FormateurAttribuerMatiere(BaseModel):
    matiere_id: UUID
    annee_scolaire_id: UUID


class FormateurAttribuerClasse(BaseModel):
    classe_id: UUID
    annee_scolaire_id: UUID


# ===========================================================================
# Parent
# ===========================================================================


class ParentCreate(BaseModel):
    name: str
    firstname: str
    email: EmailStr
    password: str
    eleve_ids: List[UUID] = []


class ParentUpdate(BaseModel):
    eleve_ids: Optional[List[UUID]] = None


class ParentResponse(OrmBase):
    id: UUID
    user: UtilisateurResponse
    eleves: List[EleveResponse] = []


# ===========================================================================
# Directeur / Administrateur / ResponsablePedagogique
# ===========================================================================


class RoleCreate(BaseModel):
    """Schéma générique pour créer un rôle (directeur, admin, resp. pédago)."""

    name: str
    firstname: str
    email: EmailStr
    password: str


class RoleResponse(OrmBase):
    id: UUID
    user: UtilisateurResponse


# ===========================================================================
# Cours
# ===========================================================================


class CoursBase(BaseModel):
    titre: str
    description: Optional[str] = None
    formateur_id: UUID
    matiere_id: UUID
    classe_id: UUID


class CoursCreate(CoursBase):
    pass


class CoursUpdate(BaseModel):
    titre: Optional[str] = None
    description: Optional[str] = None


class CoursResponse(OrmBase, CoursBase):
    id: UUID
    created_at: Optional[datetime] = None
    supports: List["SupportPedagogiqueResponse"] = []


# ===========================================================================
# SupportPedagogique
# ===========================================================================


class SupportPedagogiqueBase(BaseModel):
    nom: str
    url: str
    type: Optional[str] = None


class SupportPedagogiqueCreate(SupportPedagogiqueBase):
    pass  # cours_id fourni via le chemin URL (/cours/{id}/supports)


class SupportPedagogiqueResponse(OrmBase, SupportPedagogiqueBase):
    id: UUID
    cours_id: UUID


# ===========================================================================
# Devoir
# ===========================================================================


class DevoirBase(BaseModel):
    titre: str
    consigne: Optional[str] = None
    cours_id: Optional[UUID] = None
    classe_id: UUID
    formateur_id: UUID
    date_limite: Optional[datetime] = None


class DevoirCreate(DevoirBase):
    pass


class DevoirUpdate(BaseModel):
    titre: Optional[str] = None
    consigne: Optional[str] = None
    date_limite: Optional[datetime] = None


class DevoirResponse(OrmBase, DevoirBase):
    id: UUID
    created_at: Optional[datetime] = None


# ===========================================================================
# Soumission
# ===========================================================================


class SoumissionCreate(BaseModel):
    devoir_id: UUID
    eleve_id: UUID
    contenu: Optional[str] = None


class SoumissionCorriger(BaseModel):
    note: Optional[float] = None
    appreciation: Optional[str] = None


class SoumissionResponse(OrmBase):
    id: UUID
    devoir_id: UUID
    eleve_id: UUID
    contenu: Optional[str] = None
    note: Optional[float] = None
    appreciation: Optional[str] = None
    soumis_le: Optional[datetime] = None
    corrige_le: Optional[datetime] = None


# ===========================================================================
# Evaluation
# ===========================================================================


class EvaluationBase(BaseModel):
    titre: str
    matiere_id: UUID
    classe_id: UUID
    annee_scolaire_id: UUID
    date: Optional[datetime] = None
    bareme: int = 20


class EvaluationCreate(EvaluationBase):
    pass


class EvaluationUpdate(BaseModel):
    titre: Optional[str] = None
    date: Optional[datetime] = None
    bareme: Optional[int] = None


class EvaluationResponse(OrmBase, EvaluationBase):
    id: UUID
    notes: List["NoteResponse"] = []


# ===========================================================================
# Note
# ===========================================================================


class NoteBase(BaseModel):
    eleve_id: UUID
    evaluation_id: UUID
    valeur: float
    commentaire: Optional[str] = None


class NoteCreate(NoteBase):
    pass


class NoteBatchItem(BaseModel):
    """Un item de saisie batch (evaluation_id vient de l'URL)."""

    eleve_id: UUID
    valeur: float
    commentaire: Optional[str] = None


class NoteBatch(BaseModel):
    """Saisie de plusieurs notes d'un coup pour une évaluation."""

    notes: List[NoteBatchItem]


class NoteUpdate(BaseModel):
    valeur: Optional[float] = None
    commentaire: Optional[str] = None


class NoteResponse(OrmBase, NoteBase):
    id: UUID


# ===========================================================================
# Absence
# ===========================================================================


class AbsenceBase(BaseModel):
    eleve_id: UUID
    formateur_id: UUID
    classe_id: UUID
    annee_scolaire_id: UUID
    date: datetime
    justifiee: bool = False
    motif: Optional[str] = None


class AbsenceCreate(AbsenceBase):
    pass


class AbsenceUpdate(BaseModel):
    justifiee: Optional[bool] = None
    motif: Optional[str] = None


class AbsenceResponse(OrmBase, AbsenceBase):
    id: UUID


# ===========================================================================
# EmploiDuTemps
# ===========================================================================


class EmploiDuTempsBase(BaseModel):
    classe_id: UUID
    formateur_id: UUID
    matiere_id: UUID
    annee_scolaire_id: UUID
    jour: str
    heure_debut: str
    heure_fin: str


class EmploiDuTempsCreate(EmploiDuTempsBase):
    pass


class EmploiDuTempsUpdate(BaseModel):
    jour: Optional[str] = None
    heure_debut: Optional[str] = None
    heure_fin: Optional[str] = None


class EmploiDuTempsResponse(OrmBase, EmploiDuTempsBase):
    id: UUID


# ===========================================================================
# Annonce
# ===========================================================================


class AnnonceBase(BaseModel):
    titre: str
    contenu: str
    audience: str = "tous"


class AnnonceCreate(AnnonceBase):
    pass


class AnnonceUpdate(BaseModel):
    titre: Optional[str] = None
    contenu: Optional[str] = None
    audience: Optional[str] = None


class AnnonceResponse(OrmBase, AnnonceBase):
    id: UUID
    auteur_id: UUID
    created_at: Optional[datetime] = None


# ===========================================================================
# Notification
# ===========================================================================


class NotificationResponse(OrmBase):
    id: UUID
    user_id: UUID
    message: str
    lue: bool
    created_at: Optional[datetime] = None


# Rebuild forward refs
CoursResponse.model_rebuild()
EvaluationResponse.model_rebuild()
