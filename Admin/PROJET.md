# LACS — Logiciel d'Administration et de Contrôle Scolaire

## Table des matières

1. [Vue d'ensemble du projet](#1-vue-densemble-du-projet)
2. [Stack technique](#2-stack-technique)
3. [État actuel du code](#3-état-actuel-du-code)
4. [Problèmes identifiés dans la base de données actuelle](#4-problèmes-identifiés-dans-la-base-de-données-actuelle)
5. [Structure de base de données cible](#5-structure-de-base-de-données-cible)
6. [Logique des années scolaires](#6-logique-des-années-scolaires)
7. [Endpoints API à implémenter](#7-endpoints-api-à-implémenter)
8. [Schémas Pydantic à créer (schema.py)](#8-schémas-pydantic-à-créer-schemapy)
9. [Ce qui est fait](#9-ce-qui-est-fait)
10. [Ce qui reste à faire](#10-ce-qui-reste-à-faire)
11. [Test final — deux années scolaires](#11-test-final--deux-années-scolaires)

---

## 1. Vue d'ensemble du projet

Le **Laboratoire d'Accélération Scientifique (L.AC.S)** souhaite centraliser sa gestion académique et administrative via une application web. L'objectif est de remplacer les procédures manuelles et outils dispersés par une plateforme unique permettant :

- Le suivi des élèves et de leurs performances
- La communication entre élèves, parents, formateurs et administration
- L'automatisation des tâches administratives (notes, bulletins, listes, rapports)
- Le suivi statistique et analytique des activités pédagogiques

### Acteurs du système (7 rôles)

| Rôle                      | Description                                                                              |
|---------------------------|------------------------------------------------------------------------------------------|
| **Élève**                 | Apprenant inscrit au L.AC.S                                                              |
| **Parent**                | Responsable légal d'un ou plusieurs élèves                                               |
| **Formateur**             | Enseignant/encadreur — dispense les cours, évalue, note, enregistre les absences        |
| **Administration**        | Gère les comptes, les inscriptions, les classes, les bulletins                           |
| **Responsable pédagogique** | Supervise les cours, programmes, résultats ; valide les bulletins                      |
| **Directeur**             | Consulte les statistiques globales, publie des annonces institutionnelles                |
| **Super Administrateur**  | Configure le système, gère les rôles/permissions, sécurité, sauvegardes                 |

### Entités gérées
- Les **années scolaires** (un contexte isolé et reconfigurable)
- Les **comptes utilisateurs** (persistants entre les années)
- Les **élèves** et leurs **inscriptions annuelles**
- Les **formateurs** et leurs **attributions annuelles**
- Les **classes** (annuelles)
- Les **matières** (permanentes)
- Les **cours** et **supports pédagogiques**
- Les **devoirs** et leurs **corrections**
- Les **évaluations** et les **notes**
- Les **bulletins** (générables en PDF)
- Les **absences**
- Les **emplois du temps**
- Les **annonces** et **notifications**
- Les **parents** (un parent peut avoir plusieurs élèves)
- Les **directeurs**, **responsables pédagogiques**, **super administrateurs**

Le frontend (HTML/CSS/JS) est déjà structuré avec des sections : Dashboard, Classes, Élèves, Évaluation, Formateurs, Thème.

---

## 2. Stack technique

| Composant         | Technologie                  |
|-------------------|------------------------------|
| Backend           | FastAPI (Python)              |
| ORM               | SQLAlchemy                   |
| Migrations        | Alembic                      |
| Base de données   | PostgreSQL 16 (via Docker)   |
| Validation        | Pydantic                     |
| Auth              | JWT (à implémenter)          |
| Conteneurisation  | Docker Compose               |

**Lancer la base de données :**
```bash
docker-compose up -d
```

**Lancer le serveur :**
```bash
uvicorn app:app --reload
```

**Lancer une migration :**
```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

---

## 3. État actuel du code

### `app/__init__.py`
Instance FastAPI créée, routes importées.

### `app/database.py`
Connexion PostgreSQL via variables d'environnement, session SQLAlchemy, `Base` déclarative. Correct et fonctionnel.

### `app/models.py`
Modèles SQLAlchemy définis :
- `AnneeScolaire`
- `Utilisateur`
- `Eleve`
- `Classe`
- `Matiere`
- `Formateur`
- `Parent`
- `Directeur`
- `Administrateur`
- Tables d'association : `formateur_matiere`, `formateur_classe`

### `app/routes.py`
Seulement 2 routes :
- `GET /` — Hello World
- `GET /users/` — Liste tous les utilisateurs (sans filtre, sans schéma de retour)

### `app/schema.py`
**Vide.** Aucun schéma Pydantic n'existe encore.

### `alembic/versions/`
4 migrations existent, dont la dernière (`b3e067d588b0`) est un `pass` vide.

---

## 4. Problèmes identifiés dans la base de données actuelle

### Problème 1 — `scholar_year_id` sur `Utilisateur`
**Actuel :** La clé étrangère vers l'année scolaire est sur la table `utilisateurs`.  
**Problème :** Un `Utilisateur` est un compte global (email + mot de passe). Ce compte doit persister entre les années.  
**Correction :** Supprimer `scholar_year_id` de `Utilisateur`.

### Problème 2 — Architecture Eleve/Formateur incorrecte pour le multi-années
**Actuel :** Pas d'`annee_scolaire_id` sur `eleves`/`formateurs`, et l'idée initiale était de dupliquer l'enregistrement chaque année.  
**Problème :** Dupliquer un `Eleve` chaque année alourdit la base et déphase les identifiants (le matricule devrait être stable pour toute la scolarité).  
**Correction :**
- `Eleve` et `Formateur` deviennent des **profils permanents** (créés une seule fois)
- Ajouter un `matricule` unique sur `Eleve`
- Créer une table pivot **`inscriptions`** qui représente l'inscription d'un élève dans une classe pour une année donnée
- Pour les formateurs, les attributions annuelles sont gérées via `formateur_matiere` et `formateur_classe` en ajoutant `annee_scolaire_id` directement dans ces tables d'association

### Problème 3 — `Classe` sans `annee_scolaire_id`
**Actuel :** Une classe n'est pas rattachée à une année scolaire.  
**Correction :** Ajouter `annee_scolaire_id` sur `Classe`.

### Problème 4 — Tables d'association sans `annee_scolaire_id`
**Actuel :** `formateur_matiere` et `formateur_classe` ne portent aucune information d'année.  
**Correction :**
- Ajouter `annee_scolaire_id` dans `formateur_matiere` (PK composite : formateur_id + matiere_id + annee_scolaire_id)
- Ajouter `annee_scolaire_id` dans `formateur_classe` (PK composite : formateur_id + classe_id + annee_scolaire_id — redondant avec la classe mais utile pour les requêtes directes)
- Ainsi, chaque année on ajoute de nouvelles lignes dans ces tables sans toucher au profil du formateur

### Problème 5 — `is_ancien` mal placé
**Ancien :** `is_ancien` était prévu sur `Eleve` et `Formateur`.  
**Correction :** `is_ancien` va sur la table **`inscriptions`** pour les élèves (indique une réinscription depuis une année précédente). Pour les formateurs, la notion d'"ancien" est implicite : si un formateur a des attributions dans `formateur_classe`/`formateur_matiere` pour une année, il est actif cette année — aucun marqueur supplémentaire n'est nécessaire.

### Problème 6 — Pas de modèles `Evaluation` et `Note`
**Correction :** Créer ces deux modèles (voir section 5).

### Problème 7 — Back-populate incorrect sur `Matiere`
**Actuel :** `Matiere.formateurs` a `back_populates="formateurs"` mais du côté `Formateur` la relation s'appelle aussi `matieres`.  
**Correction :** `back_populates="matieres"` sur `Matiere` et `back_populates="formateurs"` côté `Formateur` — en cohérence.

### Problème 8 — Pas d'authentification
Aucun middleware JWT, aucune route de login/logout.

### Problème 9 — Rôle `ResponsablePedagogique` manquant
Le cahier des charges définit 7 rôles. Le modèle actuel n'a pas de table `responsables_pedagogiques`.

### Problème 10 — `Parent` lié à un seul élève
**Actuel :** `Parent.student_id` est une clé étrangère unique vers un seul élève.  
**Cahier des charges :** "Un parent peut avoir plusieurs élèves."  
**Correction :** Supprimer `student_id` de `Parent` et créer une table d'association `parent_eleve`.

### Problème 11 — Entités pédagogiques manquantes
Le cahier des charges mentionne des fonctionnalités dont les modèles n'existent pas du tout :
- `Cours` (les formateurs créent et publient des cours)
- `SupportPedagogique` (fichiers/ressources liés à un cours)
- `Devoir` (devoirs publiés par les formateurs, soumis par les élèves)
- `Soumission` (réponse d'un élève à un devoir)
- `Bulletin` (généré par classe/élève/période)
- `Absence` (enregistrement des absences par les formateurs)
- `EmploiDuTemps` (consultation par élèves, parents, formateurs)
- `Annonce` (publiée par directeurs, formateurs, administration)
- `Notification` (reçue par tous les acteurs)

---

## 5. Structure de base de données cible

### Règle générale
> `Utilisateur` = compte permanent (email, mot de passe)  
> `Eleve` = profil permanent avec matricule stable (créé une seule fois)  
> `Formateur` = profil permanent (créé une seule fois)  
> `Inscription` = pivot annuel : (élève × classe × année) — une ligne par année d'inscription  
> `formateur_matiere` / `formateur_classe` = attributions annuelles du formateur (filtrées par `annee_scolaire_id`)  
> `Classe` = entité annuelle  
> `Matiere` = entité permanente (réutilisée d'année en année)

---

### Table `annee_scolaires`
| Colonne    | Type    | Description              |
|------------|---------|--------------------------|
| `id`       | UUID PK |                          |
| `name`     | String  | Ex : "2025-2026"         |
| `is_active`| Boolean | Année en cours (une seule active à la fois) |

---

### Table `utilisateurs`
| Colonne      | Type     | Description                  |
|--------------|----------|------------------------------|
| `id`         | UUID PK  |                              |
| `name`       | String   | Nom                          |
| `firstname`  | String   | Prénom                       |
| `email`      | String   | Unique, identifiant de connexion |
| `password`   | Text     | Hash bcrypt                  |
| `created_at` | DateTime |                              |
| `updated_at` | DateTime |                              |

> Pas de `scholar_year_id` ici. Le compte persiste.

---

### Table `eleves`
| Colonne      | Type    | Description                                                 |
|--------------|---------|-------------------------------------------------------------|
| `id`         | UUID PK |                                                             |
| `user_id`    | UUID FK → `utilisateurs.id`                                 |
| `matricule`  | String  | Identifiant unique et stable (ex : "LACS-2024-001")        |

> Profil **permanent** — créé une seule fois, ne se duplique pas d'année en année.

---

### Table `inscriptions` *(pivot annuel élève)*
| Colonne             | Type     | Description                                           |
|---------------------|----------|-------------------------------------------------------|
| `id`                | UUID PK  |                                                       |
| `eleve_id`          | UUID FK → `eleves.id`                                 |
| `classe_id`         | UUID FK → `classes.id` (nullable)                     |
| `annee_scolaire_id` | UUID FK → `annee_scolaires.id`                        |
| `is_ancien`         | Boolean  | `True` si réinscrit depuis une année précédente       |
| `date_inscription`  | DateTime |                                                       |

> Une ligne par année d'inscription. Pour voir toutes les années d'un élève : `WHERE eleve_id = X`.  
> Contrainte unique : (eleve_id, annee_scolaire_id) — un élève ne peut être inscrit qu'une fois par an.

---

### Table `formateurs`
| Colonne   | Type    | Description                   |
|-----------|---------|-------------------------------|
| `id`      | UUID PK |                               |
| `user_id` | UUID FK → `utilisateurs.id`  |

> Profil **permanent** — le formateur est créé une seule fois. Ses attributions (classes, matières) changent via les tables d'association.

---

### Table `classes`
| Colonne             | Type    | Description                 |
|---------------------|---------|-----------------------------|
| `id`                | UUID PK |                             |
| `name`              | String  | Ex : "CE1", "Terminale A"   |
| `annee_scolaire_id` | UUID FK → `annee_scolaires.id` |      |

> `effectif` peut être calculé dynamiquement (COUNT des élèves de cette classe), inutile de le stocker.

---

### Table `matieres`
| Colonne | Type    | Description                  |
|---------|---------|------------------------------|
| `id`    | UUID PK |                              |
| `name`  | String  | Ex : "Mathématiques"         |

> Pas d'`annee_scolaire_id` : les matières sont globales et réutilisées d'année en année.

---

### Table d'association `formateur_matiere` *(attributions annuelles)*
| Colonne             | Type    |
|---------------------|---------|
| `formateur_id`      | UUID FK → `formateurs.id`      |
| `matiere_id`        | UUID FK → `matieres.id`        |
| `annee_scolaire_id` | UUID FK → `annee_scolaires.id` |

> PK composite : (formateur_id, matiere_id, annee_scolaire_id).  
> Chaque nouvelle année = nouvelles lignes. Les anciennes sont conservées (historique).

---

### Table d'association `formateur_classe` *(attributions annuelles)*
| Colonne             | Type    |
|---------------------|---------|
| `formateur_id`      | UUID FK → `formateurs.id`      |
| `classe_id`         | UUID FK → `classes.id`         |
| `annee_scolaire_id` | UUID FK → `annee_scolaires.id` |

> PK composite : (formateur_id, classe_id, annee_scolaire_id).  
> L'`annee_scolaire_id` ici est redondant avec celui de la `classe`, mais il facilite les requêtes directes (ex : "toutes les classes d'un formateur pour une année").

---

### Table `evaluations`
| Colonne             | Type     | Description                     |
|---------------------|----------|---------------------------------|
| `id`                | UUID PK  |                                 |
| `titre`             | String   | Intitulé de l'évaluation        |
| `matiere_id`        | UUID FK → `matieres.id`     |   |
| `classe_id`         | UUID FK → `classes.id`      |   |
| `annee_scolaire_id` | UUID FK → `annee_scolaires.id` |  |
| `date`              | DateTime | Date de passage                 |
| `bareme`            | Integer  | Note maximale (ex : 20)         |

---

### Table `notes`
| Colonne         | Type    | Description                                          |
|-----------------|---------|------------------------------------------------------|
| `id`            | UUID PK |                                                      |
| `eleve_id`      | UUID FK → `eleves.id` (profil permanent)             |
| `evaluation_id` | UUID FK → `evaluations.id`                           |
| `valeur`        | Float   | Note obtenue                                         |
| `commentaire`   | Text    | Optionnel                                            |

> L'année est implicite via `evaluation.annee_scolaire_id`.

---

### Table `parents`
| Colonne   | Type    |
|-----------|---------|
| `id`      | UUID PK |
| `user_id` | UUID FK → `utilisateurs.id` |

---

### Table `directeurs` / `administrateurs` / `responsables_pedagogiques`
| Colonne   | Type    |
|-----------|---------|
| `id`      | UUID PK |
| `user_id` | UUID FK → `utilisateurs.id` |

> Ces rôles ne sont pas annuels (ils s'appliquent globalement).

---

### Table d'association `parent_eleve`
| Colonne    | Type    |
|------------|---------|
| `parent_id`| UUID FK → `parents.id` |
| `eleve_id` | UUID FK → `eleves.id`  |

> PK composite : (parent_id, eleve_id). Un parent peut avoir plusieurs élèves (profils permanents).

---

### Table `cours`
| Colonne             | Type     | Description                          |
|---------------------|----------|--------------------------------------|
| `id`                | UUID PK  |                                      |
| `titre`             | String   |                                      |
| `description`       | Text     | Optionnel                            |
| `formateur_id`      | UUID FK → `formateurs.id`        |
| `matiere_id`        | UUID FK → `matieres.id`          |
| `classe_id`         | UUID FK → `classes.id`           |
| `annee_scolaire_id` | UUID FK → `annee_scolaires.id`   |
| `created_at`        | DateTime |                                      |

---

### Table `supports_pedagogiques`
| Colonne    | Type    | Description                                       |
|------------|---------|---------------------------------------------------|
| `id`       | UUID PK |                                                   |
| `cours_id` | UUID FK → `cours.id`                              |
| `nom`      | String  | Nom du fichier                                    |
| `url`      | String  | Chemin ou URL du fichier (PDF, image, vidéo…)     |
| `type`     | String  | Ex : "pdf", "video", "image"                      |

---

### Table `devoirs`
| Colonne             | Type     | Description                        |
|---------------------|----------|------------------------------------|
| `id`                | UUID PK  |                                    |
| `titre`             | String   |                                    |
| `consigne`          | Text     |                                    |
| `cours_id`          | UUID FK → `cours.id` (nullable)   |
| `classe_id`         | UUID FK → `classes.id`            |
| `formateur_id`      | UUID FK → `formateurs.id`         |
| `annee_scolaire_id` | UUID FK → `annee_scolaires.id`    |
| `date_limite`       | DateTime | Date de rendu                      |
| `created_at`        | DateTime |                                    |

---

### Table `soumissions`
| Colonne       | Type     | Description                             |
|---------------|----------|-----------------------------------------|
| `id`          | UUID PK  |                                         |
| `devoir_id`   | UUID FK → `devoirs.id`                  |
| `eleve_id`    | UUID FK → `eleves.id` (profil permanent)|
| `contenu`     | Text     | Texte ou lien vers le fichier soumis    |
| `note`        | Float    | Note attribuée par le formateur (nullable) |
| `appreciation`| Text     | Commentaire du formateur (nullable)     |
| `soumis_le`   | DateTime |                                         |
| `corrige_le`  | DateTime | Nullable                                |

---

### Table `absences`
| Colonne             | Type     | Description                                |
|---------------------|----------|--------------------------------------------||
| `id`                | UUID PK  |                                            |
| `eleve_id`          | UUID FK → `eleves.id` (profil permanent)   |
| `formateur_id`      | UUID FK → `formateurs.id` (profil permanent)|
| `annee_scolaire_id` | UUID FK → `annee_scolaires.id`      |
| `date`              | DateTime |                                     |
| `justifiee`         | Boolean  | `False` par défaut                  |
| `motif`             | Text     | Optionnel                           |

---

### Table `emplois_du_temps`
| Colonne             | Type    | Description                         |
|---------------------|---------|-------------------------------------|
| `id`                | UUID PK |                                     |
| `classe_id`         | UUID FK → `classes.id`              |
| `formateur_id`      | UUID FK → `formateurs.id`           |
| `matiere_id`        | UUID FK → `matieres.id`             |
| `annee_scolaire_id` | UUID FK → `annee_scolaires.id`      |
| `jour`              | String  | Ex : "Lundi"                        |
| `heure_debut`       | String  | Ex : "08:00"                        |
| `heure_fin`         | String  | Ex : "10:00"                        |

---

### Table `annonces`
| Colonne        | Type     | Description                                 |
|----------------|----------|---------------------------------------------|
| `id`           | UUID PK  |                                             |
| `titre`        | String   |                                             |
| `contenu`      | Text     |                                             |
| `auteur_id`    | UUID FK → `utilisateurs.id`                 |
| `audience`     | String   | "tous", "eleves", "parents", "formateurs"… |
| `created_at`   | DateTime |                                             |

---

### Table `notifications`
| Colonne        | Type     | Description                                |
|----------------|----------|--------------------------------------------|
| `id`           | UUID PK  |                                            |
| `user_id`      | UUID FK → `utilisateurs.id`                |
| `message`      | Text     |                                            |
| `lue`          | Boolean  | `False` par défaut                         |
| `created_at`   | DateTime |                                            |

---

### Table `bulletins`
> Les bulletins ne sont pas stockés en base, ils sont **générés dynamiquement** en PDF à partir des notes, absences et appréciations existantes. Un endpoint dédié retourne un PDF pour un élève donné sur une période donnée.

| Paramètres de génération |
|--------------------------|
| `eleve_id`               |
| `annee_scolaire_id`      |
| (optionnel) période : trimestre 1 / 2 / 3 |

---

## 6. Logique des années scolaires

### Principe fondamental
Chaque année scolaire est un **contexte indépendant**. Créer une nouvelle année ne copie rien automatiquement.

### Ce qui est **annuel** (à reconfigurer à chaque nouvelle année)
- Les **inscriptions** → nouvelle ligne dans `inscriptions` (eleve_id + classe_id + annee_scolaire_id)
- Les **classes** → re-créées pour chaque année avec `annee_scolaire_id`
- Les **attributions formateur ↔ matière** → nouvelles lignes dans `formateur_matiere` avec la nouvelle `annee_scolaire_id`
- Les **attributions formateur ↔ classe** → nouvelles lignes dans `formateur_classe` avec la nouvelle `annee_scolaire_id`
- Les **évaluations**, **notes**, **devoirs**, **absences**, **cours** → portent `annee_scolaire_id` via leur classe ou directement

### Ce qui est **permanent** (ne change pas d'année en année)
- Les **comptes utilisateurs** (`utilisateurs`) — l'email et le mot de passe ne changent pas
- Les **profils élèves** (`eleves`) — le matricule est stable pour toute la scolarité
- Les **profils formateurs** (`formateurs`) — créés une seule fois
- Les **matières** — "Mathématiques" reste "Mathématiques"
- Les **parents**, **directeurs**, **administrateurs**, **responsables pédagogiques**

### Réinscription d'un élève
1. L'admin consulte la liste des inscriptions de l'année précédente via `GET /inscriptions/?annee_scolaire_id=<ancienne>`
2. Pour réinscrire, l'API crée une **nouvelle ligne** dans `inscriptions` :
   - `eleve_id` = même élève (profil permanent inchangé)
   - `annee_scolaire_id` = nouvelle année
   - `classe_id` = null (à affecter)
   - `is_ancien = True`
3. Par défaut, **aucun élève n'est réinscrit automatiquement** lors de la création d'une nouvelle année.

### Reconfiguration des attributions d'un formateur
1. L'admin consulte les attributions de l'année précédente via `GET /formateurs/{id}/attributions?annee_scolaire_id=<ancienne>`
2. Pour reconfigurer, l'admin crée de nouvelles lignes dans `formateur_matiere` et `formateur_classe` avec la nouvelle `annee_scolaire_id`
3. Par défaut, **aucune attribution n'est copiée automatiquement** lors de la création d'une nouvelle année.

---

## 7. Endpoints API à implémenter

> Convention : tous les endpoints retournent du JSON, utilisent des schémas Pydantic.  
> Authentification : JWT Bearer Token sur tous les endpoints sauf `POST /auth/login`.

---

### Auth
| Méthode | URL              | Description                                    | Rôle requis |
|---------|------------------|------------------------------------------------|-------------|
| POST    | `/auth/login`    | Connexion, retourne un access_token JWT        | Public      |
| POST    | `/auth/logout`   | Invalider le token (blacklist ou côté client)  | Tous        |
| GET     | `/auth/me`       | Retourne l'utilisateur connecté                | Tous        |

---

### Années scolaires
| Méthode | URL                               | Description                                               |
|---------|-----------------------------------|-----------------------------------------------------------|
| GET     | `/annees-scolaires/`              | Liste toutes les années                                   |
| POST    | `/annees-scolaires/`              | Créer une nouvelle année scolaire (vide)                  |
| GET     | `/annees-scolaires/{id}`          | Détail d'une année                                        |
| PUT     | `/annees-scolaires/{id}`          | Modifier le nom                                           |
| DELETE  | `/annees-scolaires/{id}`          | Supprimer (si vide)                                       |
| PATCH   | `/annees-scolaires/{id}/activer`  | Définir cette année comme active                         |

---

### Utilisateurs (comptes)
| Méthode | URL                   | Description                            | Rôle requis   |
|---------|-----------------------|----------------------------------------|---------------|
| GET     | `/utilisateurs/`      | Liste tous les comptes                 | Admin         |
| POST    | `/utilisateurs/`      | Créer un compte utilisateur            | Admin         |
| GET     | `/utilisateurs/{id}`  | Détail d'un compte                     | Admin         |
| PUT     | `/utilisateurs/{id}`  | Modifier nom/email                     | Admin         |
| DELETE  | `/utilisateurs/{id}`  | Supprimer un compte                    | Admin         |
| PATCH   | `/utilisateurs/{id}/reset-password` | Réinitialiser le mot de passe | Admin |

---

### Élèves (profils permanents)
| Méthode | URL                         | Description                                              |
|---------|-----------------------------|----------------------------------------------------------|
| GET     | `/eleves/`                  | Liste tous les profils élèves                            |
| POST    | `/eleves/`                  | Créer un profil élève (crée `Utilisateur` si besoin + `Eleve` avec matricule) |
| GET     | `/eleves/{id}`              | Détail du profil + historique des inscriptions           |
| PUT     | `/eleves/{id}`              | Modifier le profil (nom, email…)                         |
| DELETE  | `/eleves/{id}`              | Supprimer le profil (si aucune inscription active)       |
| GET     | `/eleves/{id}/inscriptions` | Toutes les années d'inscription d'un élève               |
| GET     | `/eleves/{id}/notes?annee_scolaire_id={id}` | Notes d'un élève pour une année    |

---

### Inscriptions *(pivot élève × classe × année)*
| Méthode | URL                                              | Description                                           |
|---------|--------------------------------------------------|-------------------------------------------------------|
| GET     | `/inscriptions/?annee_scolaire_id={id}`          | Liste les inscriptions d'une année                    |
| GET     | `/inscriptions/?eleve_id={id}`                   | Toutes les inscriptions d'un élève (toutes années)    |
| POST    | `/inscriptions/`                                 | Inscrire un élève pour l'année active                 |
| POST    | `/inscriptions/reinscription`                    | Réinscrire un élève depuis une année passée (`is_ancien=True`) |
| PUT     | `/inscriptions/{id}`                             | Modifier (affecter/changer de classe)                 |
| DELETE  | `/inscriptions/{id}`                             | Désinscrire de l'année                                |

---

### Formateurs (profils permanents)
| Méthode | URL                    | Description                                                  |
|---------|------------------------|--------------------------------------------------------------|
| GET     | `/formateurs/`         | Liste tous les profils formateurs                            |
| POST    | `/formateurs/`         | Créer un profil formateur (crée `Utilisateur` si besoin)     |
| GET     | `/formateurs/{id}`     | Détail du profil                                             |
| PUT     | `/formateurs/{id}`     | Modifier le profil (nom, email…)                             |
| DELETE  | `/formateurs/{id}`     | Supprimer le profil (si aucune attribution active)           |

---

### Attributions formateurs *(annuelles)*
| Méthode | URL                                                                      | Description                                            |
|---------|--------------------------------------------------------------------------|--------------------------------------------------------|
| GET     | `/formateurs/{id}/attributions?annee_scolaire_id={id}`                   | Matières et classes du formateur pour une année        |
| POST    | `/formateurs/{id}/matieres`                                              | Assigner une matière pour une année (`annee_scolaire_id` dans le body) |
| DELETE  | `/formateurs/{id}/matieres/{matiere_id}?annee_scolaire_id={id}`          | Retirer une matière pour une année                     |
| POST    | `/formateurs/{id}/classes`                                               | Assigner une classe pour une année                     |
| DELETE  | `/formateurs/{id}/classes/{classe_id}?annee_scolaire_id={id}`            | Retirer une classe pour une année                      |
| GET     | `/formateurs/?annee_scolaire_id={id}`                                    | Liste les formateurs actifs pour une année (ayant des attributions) |

---

### Classes
| Méthode | URL                                          | Description                            |
|---------|----------------------------------------------|----------------------------------------|
| GET     | `/classes/?annee_scolaire_id={id}`           | Liste les classes d'une année          |
| POST    | `/classes/`                                  | Créer une classe (liée à l'année active) |
| GET     | `/classes/{id}`                              | Détail d'une classe + liste élèves     |
| PUT     | `/classes/{id}`                              | Modifier le nom                        |
| DELETE  | `/classes/{id}`                              | Supprimer (si vide)                    |
| GET     | `/classes/{id}/eleves`                       | Élèves d'une classe                    |
| GET     | `/classes/{id}/formateurs`                   | Formateurs d'une classe                |

---

### Matières
| Méthode | URL               | Description                  |
|---------|-------------------|------------------------------|
| GET     | `/matieres/`      | Liste toutes les matières    |
| POST    | `/matieres/`      | Créer une matière            |
| GET     | `/matieres/{id}`  | Détail                       |
| PUT     | `/matieres/{id}`  | Modifier le nom              |
| DELETE  | `/matieres/{id}`  | Supprimer                    |

---

### Évaluations
| Méthode | URL                                              | Description                               |
|---------|--------------------------------------------------|-------------------------------------------|
| GET     | `/evaluations/?annee_scolaire_id={id}`           | Liste les évaluations d'une année         |
| GET     | `/evaluations/?classe_id={id}`                   | Filtrer par classe                        |
| POST    | `/evaluations/`                                  | Créer une évaluation                      |
| GET     | `/evaluations/{id}`                              | Détail + notes                            |
| PUT     | `/evaluations/{id}`                              | Modifier                                  |
| DELETE  | `/evaluations/{id}`                              | Supprimer                                 |
| POST    | `/evaluations/{id}/notes`                        | Saisir les notes (batch pour toute la classe) |
| PUT     | `/evaluations/{id}/notes/{eleve_id}`             | Modifier la note d'un élève               |

---

### Parents
| Méthode | URL               | Description                                        |
|---------|-------------------|----------------------------------------------------|
| GET     | `/parents/`       | Liste tous les parents                             |
| POST    | `/parents/`       | Créer un parent (crée `Utilisateur` + lie à élève) |
| GET     | `/parents/{id}`   | Détail                                             |
| PUT     | `/parents/{id}`   | Modifier                                           |
| DELETE  | `/parents/{id}`   | Supprimer                                          |

---

### Directeurs / Administrateurs / Responsable pédagogique
| Méthode | URL                              | Description         |
|---------|----------------------------------|---------------------|
| GET     | `/directeurs/`                   | Liste              |
| POST    | `/directeurs/`                   | Créer              |
| DELETE  | `/directeurs/{id}`               | Supprimer          |
| GET     | `/administrateurs/`              | Liste              |
| POST    | `/administrateurs/`              | Créer              |
| DELETE  | `/administrateurs/{id}`          | Supprimer          |
| GET     | `/responsables-pedagogiques/`    | Liste              |
| POST    | `/responsables-pedagogiques/`    | Créer              |
| DELETE  | `/responsables-pedagogiques/{id}`| Supprimer          |

---

### Cours
| Méthode | URL                                            | Description                               |
|---------|------------------------------------------------|-------------------------------------------|
| GET     | `/cours/?annee_scolaire_id={id}`               | Liste les cours d'une année               |
| GET     | `/cours/?classe_id={id}`                       | Filtrer par classe                        |
| POST    | `/cours/`                                      | Créer un cours                            |
| GET     | `/cours/{id}`                                  | Détail + supports                         |
| PUT     | `/cours/{id}`                                  | Modifier                                  |
| DELETE  | `/cours/{id}`                                  | Supprimer                                 |
| POST    | `/cours/{id}/supports`                         | Ajouter un support pédagogique (upload)   |
| DELETE  | `/cours/{id}/supports/{support_id}`            | Supprimer un support                      |

---

### Devoirs
| Méthode | URL                                             | Description                                   |
|---------|-------------------------------------------------|-----------------------------------------------|
| GET     | `/devoirs/?annee_scolaire_id={id}`              | Liste les devoirs d'une année                 |
| GET     | `/devoirs/?classe_id={id}`                      | Filtrer par classe                            |
| POST    | `/devoirs/`                                     | Créer un devoir                               |
| GET     | `/devoirs/{id}`                                 | Détail + soumissions                          |
| PUT     | `/devoirs/{id}`                                 | Modifier                                      |
| DELETE  | `/devoirs/{id}`                                 | Supprimer                                     |
| POST    | `/devoirs/{id}/soumettre`                       | Élève soumet sa réponse                       |
| PUT     | `/devoirs/{id}/soumissions/{eleve_id}/corriger` | Formateur note et apprécie une soumission     |

---

### Absences
| Méthode | URL                                              | Description                          |
|---------|--------------------------------------------------|--------------------------------------|
| GET     | `/absences/?eleve_id={id}`                       | Absences d'un élève                  |
| GET     | `/absences/?classe_id={id}&date={date}`          | Absences d'une classe pour une date  |
| POST    | `/absences/`                                     | Enregistrer une absence              |
| PUT     | `/absences/{id}`                                 | Modifier (justifier, ajouter motif)  |
| DELETE  | `/absences/{id}`                                 | Supprimer                            |

---

### Emploi du temps
| Méthode | URL                                          | Description                          |
|---------|----------------------------------------------|--------------------------------------|
| GET     | `/emplois-du-temps/?classe_id={id}`          | EDT d'une classe                     |
| GET     | `/emplois-du-temps/?formateur_id={id}`       | EDT d'un formateur                   |
| POST    | `/emplois-du-temps/`                         | Créer un créneau                     |
| PUT     | `/emplois-du-temps/{id}`                     | Modifier un créneau                  |
| DELETE  | `/emplois-du-temps/{id}`                     | Supprimer un créneau                 |

---

### Annonces
| Méthode | URL                       | Description                                  |
|---------|---------------------------|----------------------------------------------|
| GET     | `/annonces/`              | Liste (filtrées selon le rôle connecté)      |
| POST    | `/annonces/`              | Publier une annonce                          |
| GET     | `/annonces/{id}`          | Détail                                       |
| PUT     | `/annonces/{id}`          | Modifier                                     |
| DELETE  | `/annonces/{id}`          | Supprimer                                    |

---

### Notifications
| Méthode | URL                              | Description                             |
|---------|----------------------------------|-----------------------------------------|
| GET     | `/notifications/`                | Mes notifications (utilisateur connecté)|
| PATCH   | `/notifications/{id}/lire`       | Marquer comme lue                       |
| PATCH   | `/notifications/lire-tout`       | Tout marquer comme lu                   |

---

### Bulletins (génération PDF)
| Méthode | URL                                                          | Description                          |
|---------|--------------------------------------------------------------|--------------------------------------|
| GET     | `/bulletins/{eleve_id}?annee_scolaire_id={id}`               | Générer/télécharger le bulletin PDF  |
| GET     | `/bulletins/classe/{classe_id}?annee_scolaire_id={id}`       | Bulletins de toute une classe (ZIP)  |

---

## 8. Schémas Pydantic à créer (`schema.py`)

Pour chaque entité, créer 3 types de schémas :

- `XxxBase` — champs communs de création/modification
- `XxxCreate` — hérite de Base, utilisé en entrée `POST`
- `XxxResponse` — hérite de Base + `id`, utilisé en sortie (avec `model_config = ConfigDict(from_attributes=True)`)

**Exemple pour `AnneeScolaire` :**
```python
class AnneeScolaireBase(BaseModel):
    name: str

class AnneeScolaireCreate(AnneeScolaireBase):
    pass

class AnneeScolaireResponse(AnneeScolaireBase):
    id: UUID
    is_active: bool
    model_config = ConfigDict(from_attributes=True)
```

**Schémas à créer :**
- `AnneeScolaire` (Base, Create, Response)
- `Utilisateur` (Base, Create, Response — sans mot de passe en sortie)
- `UtilisateurLogin` (email + password)
- `Token` (access_token, token_type)
- `Eleve` (Base, Create, Response — avec `matricule`, embarque `UtilisateurResponse`)
- `Inscription` (Base, Create, Response — avec `is_ancien`)
- `Formateur` (Base, Create, Response)
- `FormateurAttributions` (Response — matières + classes pour une année)
- `Classe` (Base, Create, Response — avec `effectif` calculé)
- `Matiere` (Base, Create, Response)
- `Cours` (Base, Create, Response)
- `SupportPedagogique` (Base, Create, Response)
- `Devoir` (Base, Create, Response)
- `Soumission` (Base, Create, Response)
- `Evaluation` (Base, Create, Response)
- `Note` (Base, Create, Response)
- `Absence` (Base, Create, Response)
- `EmploiDuTemps` (Base, Create, Response)
- `Annonce` (Base, Create, Response)
- `Notification` (Response)
- `Parent` (Base, Create, Response)
- `ResponsablePedagogique` (Base, Create, Response)

---

## 9. Ce qui est fait

| Élément                                     | État        |
|---------------------------------------------|-------------|
| Structure du projet FastAPI                  | ✅ Fait     |
| Connexion PostgreSQL (database.py)           | ✅ Fait     |
| Docker Compose PostgreSQL                    | ✅ Fait     |
| Alembic configuré + `alembic.ini` corrigé   | ✅ Fait     |
| `app/models.py` — architecture complète     | ✅ Fait     |
| `app/schema.py` — tous les schémas Pydantic v2 | ✅ Fait  |
| `app/auth.py` — JWT + bcrypt + require_roles | ✅ Fait    |
| `app/routes.py` — tous les endpoints        | ✅ Fait     |
| Migration `refactor_architecture_pivot_inscription` | ✅ Générée et appliquée |
| Dépendances installées (python-jose, passlib, multipart, email-validator) | ✅ Fait |
| Serveur démarrant sans erreur               | ✅ Vérifié  |
| `SUIVI.md` créé                             | ✅ Fait     |

---

## 10. Ce qui reste à faire

### Phase 1 — Correction du modèle de données ✅ TERMINÉ

**Profils permanents :**
- [x] Supprimer `scholar_year_id` de `Utilisateur`
- [x] Retirer `annee_scolaire_id` et `is_ancien` de `Eleve` (profil permanent)
- [x] Ajouter `matricule` (String, unique) sur `Eleve`
- [x] Retirer `annee_scolaire_id` et `is_ancien` de `Formateur` (profil permanent)

**Nouvelles tables :**
- [x] Créer le modèle `Inscription` (pivot annuel)
- [x] Supprimer `student_id` de `Parent` + créer la table `parent_eleve`
- [x] Créer le modèle `ResponsablePedagogique`
- [x] Créer tous les modèles pédagogiques (Evaluation, Note, Cours, SupportPedagogique, Devoir, Soumission, Absence, EmploiDuTemps, Annonce, Notification)

**Tables corrigées :**
- [x] Ajouter `annee_scolaire_id` sur `Classe`
- [x] Ajouter `is_active` (Boolean) sur `AnneeScolaire`
- [x] Supprimer `effectif` de `Classe` (calculé dynamiquement)
- [x] Modifier `formateur_matiere` et `formateur_classe` avec PK composites incluant `annee_scolaire_id`
- [x] Corriger les `back_populates`
- [x] Générer et appliquer la migration Alembic

### Phase 2 — Schémas Pydantic ✅ TERMINÉ

- [x] Tous les schémas Base/Create/Update/Response pour chaque entité
- [x] Schéma `Token` et `UtilisateurLogin`
- [x] Schémas spéciaux (NoteBatch, SoumissionCorriger, FormateurAttribuerMatiere/Classe, InscriptionReinscription)

### Phase 3 — Authentification ✅ TERMINÉ

- [x] `python-jose[cryptography]` et `passlib[bcrypt]` installés
- [x] Hashage bcrypt des mots de passe
- [x] Logique JWT (créer/vérifier un token)
- [x] `POST /auth/login`
- [x] Middleware `get_current_user`
- [x] Protection des routes avec `require_roles(*roles)`

### Phase 4 — Implémentation des endpoints ✅ TERMINÉ

- [x] Années scolaires (CRUD + activer)
- [x] Auth (login, me)
- [x] Utilisateurs (CRUD + reset password)
- [x] Élèves — profils (CRUD + matricule)
- [x] Inscriptions — pivot annuel (CRUD + réinscription)
- [x] Formateurs — profils (CRUD)
- [x] Formateurs — attributions annuelles (assigner/retirer matières et classes par année)
- [x] Classes (CRUD + consultation élèves/formateurs)
- [x] Matières (CRUD)
- [x] Cours (CRUD + supports)
- [x] Devoirs (CRUD + soumissions + corrections)
- [x] Évaluations (CRUD)
- [x] Notes (saisie batch + modification)
- [x] Absences (CRUD)
- [x] Emploi du temps (CRUD)
- [x] Annonces (CRUD)
- [x] Notifications (liste + marquer lue)
- [x] Parents (CRUD)
- [x] Directeurs / Administrateurs / Responsables pédagogiques (CRUD)
- [ ] Bulletins (génération PDF) — à implémenter

### Phase 5 — Qualité et sécurité (à faire)

- [x] Le mot de passe n'est jamais retourné dans les réponses (non inclus dans `UtilisateurResponse`)
- [x] Gestion des erreurs HTTP propres (404, 403, 409 pour conflits)
- [x] Validation des emails avec Pydantic `EmailStr`
- [x] Respect de la hiérarchie des rôles (permissions par endpoint)
- [ ] Pagination sur les listes (`skip`, `limit`)
- [ ] Exportation bulletins en PDF (`reportlab` ou `weasyprint`)
- [ ] Exportation listes en Excel (`openpyxl`)
- [ ] Protection des données : seul un parent peut voir les résultats de ses propres enfants
- [ ] Tests automatisés (pytest + httpx)

---

## 11. Test final — deux années scolaires

À la fin du développement, un test de bout en bout sera réalisé pour valider le comportement multi-années :

### Scénario de test

#### Année 1 — "2024-2025"
1. Créer l'année scolaire "2024-2025" et l'activer
2. Créer 3 matières : Mathématiques, Français, Sciences
3. Créer 2 classes : "6ème A", "6ème B"
4. Créer 2 formateurs (avec comptes utilisateurs) et les assigner aux classes/matières
5. Créer 5 élèves et les répartir dans les classes
6. Créer une évaluation en Mathématiques pour "6ème A"
7. Saisir les notes des 5 élèves
8. Vérifier via `GET /eleves/?annee_scolaire_id=<id_2024>` → 5 élèves retournés
9. Vérifier via `GET /evaluations/?annee_scolaire_id=<id_2024>` → 1 évaluation retournée

#### Année 2 — "2025-2026"
1. Créer l'année scolaire "2025-2026" et l'activer
2. Vérifier via `GET /inscriptions/?annee_scolaire_id=<id_2025>` → **0 inscriptions** (année vide)
3. Vérifier via `GET /formateurs/?annee_scolaire_id=<id_2025>` → **0 formateurs actifs** (aucune attribution)
4. Recréer les classes "6ème A" et "6ème B" pour cette année
5. Réinscrire 3 des 5 élèves : `POST /inscriptions/reinscription` → `is_ancien=True`, `classe_id=null`
6. Affecter les 3 élèves réinscrits à leurs nouvelles classes
7. Reconfigurer les attributions du formateur 1 pour la nouvelle année : `POST /formateurs/{id}/classes` + `POST /formateurs/{id}/matieres`
8. Créer 1 nouveau profil élève + l'inscrire → `is_ancien=False`
9. Créer une évaluation en Français pour "6ème A" sur cette nouvelle année

#### Vérifications croisées
- `GET /inscriptions/?annee_scolaire_id=<id_2024>` → 5 inscriptions (données année 1 intactes)
- `GET /inscriptions/?annee_scolaire_id=<id_2025>` → 4 inscriptions (3 avec `is_ancien=True`, 1 avec `is_ancien=False`)
- `GET /eleves/` → toujours **5 profils** (les profils sont permanents, aucun n'a été recréé)
- `GET /eleves/{id}/inscriptions` → historique sur 2 ans pour les élèves réinscrits
- `GET /evaluations/?annee_scolaire_id=<id_2024>` → 1 évaluation (Maths)
- `GET /evaluations/?annee_scolaire_id=<id_2025>` → 1 évaluation (Français)
- Les **matières** sont communes aux deux années (aucun doublon)
- Les **formateurs** sont les mêmes profils mais avec des attributions différentes selon l'année

---

*Document généré le 12 mars 2026 — à mettre à jour au fil du développement.*
