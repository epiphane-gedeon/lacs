# SUIVI DE DÉVELOPPEMENT — LACS Admin

## Session du 12 mars 2026

### Ce qui a été accompli

#### Phase 1 — Documentation

- [x] Analyse complète du cahier des charges (PDF 9 pages extrait via pdfplumber)
- [x] Analyse du code existant (models, routes, schema, app, database, alembic, docker)
- [x] Création de `PROJET.md` — documentation exhaustive du projet

#### Phase 2 — Refactorisation de l'architecture

**Problèmes identifiés et décisions prises :**

| # | Problème | Solution retenue |
|---|----------|-----------------|
| 1 | `scholar_year_id` dans `Utilisateur` | Supprimé (l'utilisateur est permanent) |
| 2 | `Eleve`/`Formateur` recréés chaque année | Profils permanents + pivot `Inscription` |
| 3 | Pas de matricule pour les élèves | `matricule` unique ajouté à `Eleve` |
| 4 | Pas de table pivot pour les inscriptions | Table `Inscription` créée (pivot annuel) |
| 5 | `Classe` sans `annee_scolaire_id` | `annee_scolaire_id` ajouté à `Classe` |
| 6 | Attribution Formateur sans notion d'année | `annee_scolaire_id` ajouté aux clés composites `formateur_matiere` et `formateur_classe` |
| 7 | `is_ancien` sur `Eleve` | Déplacé dans `Inscription` |
| 8 | Pas de `is_active` sur `AnneeScolaire` | Ajouté |
| 9 | `effectif` en dur dans `Classe` | Supprimé, calculé dynamiquement (`len(classe.inscriptions)`) |
| 10 | `student_id` dans `Parent` (lien 1-1) | Remplacé par table `parent_eleve` (M-M) |
| 11 | `ResponsablePedagogique` manquant | Modèle créé |
| 12 | 9 modèles pédagogiques manquants | Tous créés (`Cours`, `SupportPedagogique`, `Devoir`, `Soumission`, `Evaluation`, `Note`, `Absence`, `EmploiDuTemps`, `Annonce`, `Notification`) |
| 13 | `back_populates` incorrects | Tous corrigés |
| 14 | UUID sans `as_uuid=True` | Corrigé partout |

#### Phase 3 — Implémentation backend

**Fichiers modifiés :**

| Fichier | Statut | Détail |
|---------|--------|--------|
| `requirements.txt` | ✅ Mis à jour | python-jose[cryptography], passlib[bcrypt], python-multipart, pydantic[email] |
| `app/models.py` | ✅ Réécrit | 16 modèles + 3 tables d'association |
| `app/schema.py` | ✅ Réécrit | Tous les schémas Pydantic v2 (~450 lignes) |
| `app/auth.py` | ✅ Créé | JWT HS256 + bcrypt + middleware d'autorisation par rôles |
| `app/routes.py` | ✅ Réécrit | Tous les endpoints (~650 lignes) |
| `alembic.ini` | ✅ Corrigé | `sqlalchemy.url` pointait vers `mydatabase` → corrigé vers `postgres` |
| `alembic/versions/1299f2bb0f74_refactor_architecture_pivot_inscription.py` | ✅ Généré et appliqué | Migration auto-générée, appliquée avec succès |

**Dépendances installées dans le venv :**
```
python-jose[cryptography]==3.x
passlib[bcrypt]==1.x
python-multipart
email-validator
```

**Serveur testé :** `uvicorn app:app --port 8080` → démarrage OK, aucune erreur

---

## Architecture finale

### Modèles SQLAlchemy

```
Utilisateur (profil de connexion)
├── Eleve          (profil permanent, 1-1 avec Utilisateur)
├── Formateur      (profil permanent, 1-1 avec Utilisateur)
├── Parent         (profil permanent, M-M avec Eleve via parent_eleve)
├── Directeur      (1-1 avec Utilisateur)
├── Administrateur (1-1 avec Utilisateur)
└── ResponsablePedagogique (1-1 avec Utilisateur)

AnneeScolaire (is_active)
├── Classe (annee_scolaire_id)
│   ├── Inscription (eleve_id, classe_id, annee_scolaire_id, is_ancien)
│   ├── Cours → SupportPedagogique, Devoir → Soumission
│   ├── Evaluation → Note
│   ├── Absence
│   └── EmploiDuTemps

formateur_matiere (formateur_id, matiere_id, annee_scolaire_id) — PK composite
formateur_classe  (formateur_id, classe_id, annee_scolaire_id) — PK composite

Annonce, Notification
```

### Endpoints API

| Groupe | Préfixe | Endpoints |
|--------|---------|-----------|
| Auth | `/auth` | POST /login, GET /me |
| Années scolaires | `/annees-scolaires` | CRUD + PATCH /activer |
| Utilisateurs | `/utilisateurs` | CRUD + PATCH /reset-password |
| Élèves | `/eleves` | CRUD + GET /inscriptions + GET /notes |
| Inscriptions | `/inscriptions` | CRUD + POST /reinscription |
| Classes | `/classes` | CRUD + GET /eleves + GET /formateurs |
| Matières | `/matieres` | CRUD |
| Formateurs | `/formateurs` | CRUD + attribution matieres/classes + GET /attributions |
| Parents | `/parents` | CRUD |
| Rôles | `/directeurs`, `/administrateurs`, `/responsables-pedagogiques` | CRUD |
| Cours | `/cours` | CRUD + supports pédagogiques |
| Devoirs | `/devoirs` | CRUD + soumettre + corriger |
| Évaluations | `/evaluations` | CRUD + batch notes + update note |
| Absences | `/absences` | CRUD |
| Emploi du temps | `/emplois-du-temps` | CRUD |
| Annonces | `/annonces` | CRUD (filtrées par rôle) |
| Notifications | `/notifications` | GET + PATCH lire/lire-tout |

### Sécurité

- Authentification JWT HS256 via `Authorization: Bearer <token>`
- Hachage bcrypt pour les mots de passe
- `require_roles("role1", "role2")` sur chaque endpoint sensible
- `get_current_user` requis sur tous les endpoints non-publics
- Pas de credentials en dur (SECRET_KEY depuis .env)

---

## Ce qui reste à faire

### Back-end
- [ ] Endpoint de génération de bulletin (PDF)
- [ ] Notifications push automatiques (ex: lors d'une absence, d'une note)
- [ ] Pagination sur les listes (`skip`, `limit`)
- [ ] Tests automatisés (pytest + httpx)
- [ ] Validation des données métier (ex: date_fin > date_debut pour AnneeScolaire)

### Front-end (`front/`)
- [ ] Intégration de l'interface existante avec l'API
- [ ] Login (stockage du JWT en localStorage)
- [ ] Gestion des rôles côté UI
- [ ] Toutes les pages fonctionnelles

### Déploiement
- [ ] Fichier `.env` de production
- [ ] Variables d'environnement Docker
- [ ] CORS configuré pour le domaine de production
- [ ] HTTPS / reverse proxy (nginx)

---

## Notes techniques

- Le serveur se lance avec : `uvicorn app:app --reload`  
  (ou `--port 8080` si le port 8000 est occupé par Docker)
- Base de données : PostgreSQL 16 dans Docker (`docker compose up -d`)
- Migrations : `alembic upgrade head`
- Docs interactives : http://localhost:8080/docs (Swagger) ou /redoc
- Toujours activer une AnneeScolaire avant de créer des inscriptions/classes
