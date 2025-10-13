# 📧 Configuration Email LACS - Guide Complet

## ✅ Fonctionnalités implémentées

### 🎯 Système d'envoi avec fallback
- **Email principal** : egpouli@epiphane-gedeon.com
- **Email de secours** : egpouli@gmail.com
- **Logique** : Si l'envoi vers l'email principal échoue, le système essaie automatiquement l'email Gmail

### 📝 Formulaire de contact intégré
- Formulaire Flask-WTF avec validation
- Champs : Prénom, Nom, Email, Téléphone, Sujet, Message
- Validation côté serveur et affichage des erreurs
- Messages de confirmation/erreur avec Flask flash

## 🔧 Configuration requise

### 1. Paramètres SMTP dans `app/__init__.py`
```python
# Remplacez ces valeurs par vos vraies informations
app.config['MAIL_USERNAME'] = 'votre-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'votre-mot-de-passe-app'
```

### 2. Configuration Gmail (Recommandée)
1. **Activez l'authentification à 2 facteurs** sur votre compte Gmail
2. **Générez un mot de passe d'application** :
   - Allez dans Paramètres > Sécurité > Authentification à 2 facteurs
   - Cliquez sur "Mots de passe des applications"
   - Générez un nouveau mot de passe pour "LACS Website"
3. **Utilisez ce mot de passe** dans `MAIL_PASSWORD`

### 3. Alternative avec un serveur SMTP personnalisé
```python
app.config['MAIL_SERVER'] = 'votre-serveur-smtp.com'
app.config['MAIL_PORT'] = 587  # ou 465 pour SSL
app.config['MAIL_USE_TLS'] = True  # ou False pour SSL
```

## 🧪 Test du système

### Tester localement
```bash
python test_email.py
```

### Tester via le site
1. Lancez l'application : `flask run`
2. Allez sur `/contact`
3. Remplissez et soumettez le formulaire
4. Vérifiez les messages de confirmation

## 📨 Format des emails reçus

```
Sujet: [LACS Contact] Demande d'information

Nouvelle demande de contact depuis le site LACS :

Informations du contact :
- Nom : Dupont
- Prénom : Jean
- Email : jean.dupont@exemple.com
- Téléphone : +228 12 34 56 78
- Sujet : Demande d'information

Message :
Votre message ici...

---
Ce message a été envoyé depuis le formulaire de contact du site LACS.
Vous pouvez répondre directement à l'adresse : jean.dupont@exemple.com
```

## 🔄 Logique de fallback

1. **Tentative principale** → egpouli@epiphane-gedeon.com
2. **Si échec** → egpouli@gmail.com  
3. **Si les deux échouent** → Message d'erreur à l'utilisateur

## 🛠️ Débogage

### Activer les logs email
```python
app.config['MAIL_DEBUG'] = True
```

### Vérifier la configuration
```python
from app import app, mail
with app.app_context():
    print(f"MAIL_SERVER: {app.config['MAIL_SERVER']}")
    print(f"MAIL_PORT: {app.config['MAIL_PORT']}")
    print(f"MAIL_USERNAME: {app.config['MAIL_USERNAME']}")
```

## 📝 Notes importantes

- **Sécurité** : Ne jamais commiter les vrais mots de passe dans le code
- **Variables d'environnement** : Utilisez `.env` pour les credentials en production
- **SSL/TLS** : Gmail nécessite TLS (port 587) ou SSL (port 465)
- **Limitations** : Gmail a des limites d'envoi (500 emails/jour pour les comptes gratuits)

## ✅ Status actuel

- ✅ Flask-Mail installé et configuré
- ✅ Formulaire de contact fonctionnel
- ✅ Validation des champs implémentée
- ✅ Système de fallback prêt
- ✅ Messages flash intégrés
- ⚠️ Credentials SMTP à configurer

## 🚀 Prochaines étapes

1. Configurer les vraies credentials SMTP
2. Tester l'envoi réel d'emails
3. Optionnel : Ajouter des templates HTML pour les emails
4. Optionnel : Sauvegarder les messages en base de données