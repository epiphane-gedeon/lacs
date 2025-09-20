# Photothèque L.AC.S

## Structure des dossiers

Pour organiser les photos de la galerie, placez vos images dans les dossiers correspondants :

### `/cours/`
- Photos des cours et formations
- Exemples : cours-maths.jpg, formation-python.jpg, cours-physique.jpg, tp-svt.jpg

### `/evenements/`
- Photos des événements spéciaux
- Exemples : portes-ouvertes.jpg, remise-prix.jpg, conference.jpg, fete-fin-annee.jpg

### `/etudiants/`
- Photos de la vie étudiante
- Exemples : groupe-etude.jpg, pause-detente.jpg, reussite-bac.jpg, nouveaux-eleves.jpg

### `/installations/`
- Photos des installations et espaces
- Exemples : salle-cours.jpg, laboratoire.jpg, espace-info.jpg, bibliotheque.jpg

## Format recommandé

- **Résolution :** 1200x800 pixels minimum
- **Formats supportés :** JPG, PNG, WebP
- **Taille :** Maximum 2MB par image
- **Ratio :** 3:2 ou 4:3 recommandé

## Comment ajouter des photos

1. Placez vos images dans le bon dossier selon la catégorie
2. Nommez vos fichiers de manière descriptive (ex: `cours-mathematiques-2024.jpg`)
3. Mettez à jour la route `phototheque()` dans `routes.py` avec les nouveaux noms de fichiers
4. Les images sont automatiquement affichées dans la galerie

## Fonctionnalités

- **Navigation par onglets** : Filtrage par catégorie
- **Lightbox** : Visualisation en plein écran
- **Navigation clavier** : Flèches et Échap
- **Responsive** : Adaptatif mobile et desktop
- **Animations** : Effets AOS au scroll
- **Fallback** : Image par défaut si photo manquante