# 🔧 Configuration Email Domaine Privé - Guide Complet

## 🎯 Objectif
Utiliser `egpouli@epiphane-gedeon.com` comme adresse d'expédition des emails du site LACS.

## 📋 Informations Nécessaires

### 1. **Paramètres SMTP de votre hébergeur**
Vous devez récupérer ces informations auprès de votre hébergeur de domaine :

```
Serveur SMTP : mail.epiphane-gedeon.com (ou smtp.epiphane-gedeon.com)
Port SMTP    : 587 (STARTTLS) ou 465 (SSL) ou 25 (non-sécurisé)
Sécurité     : STARTTLS ou SSL/TLS
Utilisateur  : egpouli@epiphane-gedeon.com
Mot de passe : [mot de passe de votre email]
```

### 2. **Hébergeurs Populaires et leurs Paramètres**

#### **OVH/OVHcloud**
```python
app.config["MAIL_SERVER"] = "ssl0.ovh.net"  # ou mail.epiphane-gedeon.com
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
```

#### **Hostinger** 
```python
app.config["MAIL_SERVER"] = "mail.epiphane-gedeon.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
```

#### **cPanel (hébergement classique)**
```python
app.config["MAIL_SERVER"] = "mail.epiphane-gedeon.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
```

#### **Google Workspace (si vous utilisez Gmail Pro)**
```python
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "egpouli@epiphane-gedeon.com"
app.config["MAIL_PASSWORD"] = "mot-de-passe-app"  # Mot de passe d'application
```

## 🔍 **Comment Trouver vos Paramètres SMTP**

### Méthode 1 : Panel d'administration
1. Connectez-vous à votre panel d'hébergement
2. Cherchez "Email" ou "Mail" 
3. Regardez les paramètres SMTP/IMAP

### Méthode 2 : Support hébergeur
Contactez votre hébergeur et demandez :
- Serveur SMTP sortant
- Port SMTP 
- Type de sécurité (TLS/SSL)

### Méthode 3 : Test automatique
Utilisez votre client email (Outlook, Thunderbird) pour configurer le compte.
Les paramètres détectés automatiquement sont souvent les bons.

## ⚙️ **Configuration dans LACS**

### Option A : Serveur SMTP Direct (Recommandé)
```python
# Dans app/__init__.py
app.config["MAIL_SERVER"] = "mail.epiphane-gedeon.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "egpouli@epiphane-gedeon.com"
app.config["MAIL_PASSWORD"] = "votre-mot-de-passe"
app.config["MAIL_DEFAULT_SENDER"] = "LACS Contact <egpouli@epiphane-gedeon.com>"
```

### Option B : Gmail avec Alias (Alternative)
Si l'Option A ne marche pas, gardez Gmail mais changez l'expéditeur apparent :
```python
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "serveurgak@gmail.com"
app.config["MAIL_PASSWORD"] = "phdc twxj phhu kfyw"
app.config["MAIL_DEFAULT_SENDER"] = "LACS Contact <egpouli@epiphane-gedeon.com>"
```

## 🧪 **Test de Configuration**

### 1. Script de Test SMTP
```python
# test_smtp_config.py
from app import app, mail
from flask_mail import Message

with app.app_context():
    try:
        msg = Message(
            subject="Test SMTP LACS",
            recipients=["egpouli@gmail.com"],  # Votre email de test
            body="Ceci est un test du serveur SMTP",
            sender=app.config["MAIL_DEFAULT_SENDER"]
        )
        mail.send(msg)
        print("✅ Email envoyé avec succès !")
    except Exception as e:
        print(f"❌ Erreur: {e}")
```

### 2. Test depuis le Site
```bash
flask run
# Testez le formulaire de contact
```

## 🔧 **Dépannage Courant**

### Erreur : "Authentication failed"
- Vérifiez username/password
- Vérifiez si l'email existe bien

### Erreur : "Connection refused" 
- Vérifiez le serveur SMTP et le port
- Testez les ports : 587, 465, 25

### Erreur : "Certificate verification failed"
```python
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USE_TLS"] = True
# ou
app.config["MAIL_USE_SSL"] = True  
app.config["MAIL_USE_TLS"] = False
```

### Emails marqués comme SPAM
- Configurez SPF/DKIM/DMARC sur votre domaine
- Utilisez un serveur SMTP réputé

## 📞 **Aide Spécifique**

### Qui contacter ?
1. **Support de votre hébergeur** (pour paramètres SMTP)
2. **Administrateur domaine** (si ce n'est pas vous)
3. **Support technique** de votre registrar de domaine

### Informations à fournir :
- Nom de domaine : `epiphane-gedeon.com`
- Email voulu : `egpouli@epiphane-gedeon.com`  
- Usage : "Envoi d'emails depuis application web Python/Flask"

## ✅ **Checklist Finale**

- [ ] Paramètres SMTP récupérés auprès de l'hébergeur
- [ ] Configuration mise à jour dans `app/__init__.py`
- [ ] Test d'envoi réussi
- [ ] Emails reçus dans la bonne boîte
- [ ] Expéditeur affiché : `egpouli@epiphane-gedeon.com`

Une fois configuré, vos emails apparaîtront comme envoyés depuis votre adresse professionnelle ! 🎯