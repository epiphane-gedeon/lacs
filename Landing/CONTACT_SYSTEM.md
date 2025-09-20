# 📧 Système d'Email LACS - Documentation Complète

## ✅ Fonctionnalités Implémentées

### 🎯 **Double Contact System**
1. **Page Contact Dédiée** (`/contact`)
   - Formulaire complet avec sélection de sujets
   - Validation avancée des champs
   - Messages flash informatifs

2. **Formulaire Page d'Accueil** (`/`)
   - Formulaire simplifié intégré en bas de page
   - Champ sujet libre (texte)
   - Design cohérent avec le site

### 📬 **Système d'Envoi avec Fallback**
- **Email principal** : `egpouli@epiphane-gedeon.com`
- **Email de secours** : `egpouli@gmail.com`
- **Logique** : Tentative automatique sur le second email si le premier échoue

## 🔧 Configuration

### 1. **Credentials SMTP** (dans `app/__init__.py`)
```python
app.config['MAIL_USERNAME'] = 'votre-email-expediteur@gmail.com'
app.config['MAIL_PASSWORD'] = 'mot-de-passe-app-gmail'
```

### 2. **Destinataires** (dans `app/routes.py`)
- Page contact : Utilise les choix prédéfinis de sujets
- Page accueil : Sujet libre dans le titre de l'email

## 📱 **Emplacements des Formulaires**

### **Page d'Accueil** (`http://localhost:5000/`)
- Formulaire en bas de page (section contact)
- Champs : Prénom, Nom, Email, Téléphone, Sujet (texte libre), Message
- Design intégré au thème du site

### **Page Contact** (`http://localhost:5000/contact`)
- Formulaire complet dédié
- Champs : Prénom, Nom, Email, Téléphone, Sujet (liste), Message
- Page avec informations de contact complètes

## 📨 **Format des Emails**

### Depuis la Page d'Accueil
```
Sujet: [LACS Contact] [Sujet saisi par l'utilisateur]

Nouvelle demande de contact depuis la page d'accueil du site LACS :
- Nom : [Nom]
- Prénom : [Prénom] 
- Email : [Email]
- Téléphone : [Téléphone]
- Sujet : [Sujet libre]
- Message : [Message]
```

### Depuis la Page Contact
```
Sujet: [LACS Contact] [Type de demande sélectionné]

Nouvelle demande de contact depuis le site LACS :
- Nom : [Nom]
- Prénom : [Prénom]
- Email : [Email] 
- Téléphone : [Téléphone]
- Sujet : [Sujet sélectionné]
- Message : [Message]
```

## 🚀 **Test du Système**

### Test Page d'Accueil
```bash
python test_contact_home.py
```

### Test Page Contact
```bash
python test_email.py
```

### Test En Ligne
1. Configurez les credentials SMTP
2. Lancez : `flask run`
3. Testez les deux formulaires

## 🔄 **Workflow Complet**

1. **Visiteur** remplit un formulaire (accueil ou contact)
2. **Validation** Flask-WTF côté serveur
3. **Envoi email** vers `egpouli@epiphane-gedeon.com`
4. **Si échec** → Tentative vers `egpouli@gmail.com`
5. **Message** de confirmation ou d'erreur affiché

## 📋 **Fichiers Modifiés**

### Backend
- ✅ `app/__init__.py` - Configuration Flask-Mail
- ✅ `app/forms.py` - ContactForm + SimpleContactForm
- ✅ `app/routes.py` - Routes `/` et `/contact` avec envoi email

### Frontend  
- ✅ `app/templates/contact.html` - Formulaire Flask-WTF
- ✅ `app/templates/index.html` - Formulaire intégré + messages flash

### Configuration
- ✅ `requirements.txt` - Flask-Mail ajouté
- ✅ `config_email.py` - Configuration email
- ✅ `EMAIL_SETUP.md` - Guide de configuration

### Tests
- ✅ `test_email.py` - Test page contact
- ✅ `test_contact_home.py` - Test page accueil

## 🎯 **Status Final**

- ✅ **Formulaire page d'accueil** opérationnel
- ✅ **Formulaire page contact** opérationnel  
- ✅ **Système de fallback email** implémenté
- ✅ **Validation des formulaires** fonctionnelle
- ✅ **Messages flash** intégrés
- ⚠️ **Credentials SMTP** à configurer pour l'envoi réel

## 🔑 **Prochaines Étapes**

1. **Configurer les vraies credentials Gmail**
2. **Tester l'envoi réel d'emails**
3. **Optionnel** : Sauvegarder les messages en base de données
4. **Optionnel** : Templates HTML pour les emails