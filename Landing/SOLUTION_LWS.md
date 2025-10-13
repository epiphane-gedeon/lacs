# 🎯 Configuration SMTP LWS - Solution pour egpouli@epiphane-gedeon.com

## ✅ **Serveur SMTP Détecté : LWS Hosting**

Votre domaine `epiphane-gedeon.com` est hébergé chez **LWS Hosting** (`web56.lws-hosting.com`).

## 🔧 **Configuration Correcte pour LWS**

```python
# Dans app/__init__.py
app.config["MAIL_SERVER"] = "mail.epiphane-gedeon.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "egpouli@epiphane-gedeon.com"
app.config["MAIL_PASSWORD"] = "LE-VRAI-MOT-DE-PASSE-EMAIL"  # ⚠️ À REMPLACER
app.config["MAIL_DEFAULT_SENDER"] = "LACS Contact <egpouli@epiphane-gedeon.com>"
```

## 🔑 **Action Requise : Mot de Passe Email**

### Le problème actuel :
```
Erreur: (535, 'Incorrect authentication data')
```

Cela signifie que le mot de passe est incorrect.

### Solutions :

#### **1. Vérifiez le mot de passe de l'email**
- Connectez-vous au webmail : `https://webmail.epiphane-gedeon.com`
- Ou via le panel LWS
- Utilisez le même mot de passe dans la configuration

#### **2. Créer l'email s'il n'existe pas**
Si `egpouli@epiphane-gedeon.com` n'existe pas encore :

1. **Connectez-vous au panel LWS**
2. **Allez dans "Emails" ou "Comptes email"**
3. **Créez l'adresse :** `egpouli@epiphane-gedeon.com`
4. **Définissez un mot de passe fort**
5. **Utilisez ce mot de passe dans la config**

#### **3. Paramètres alternatifs LWS**
Si le port 587 ne marche pas, essayez :

```python
# Option SSL (port 465)
app.config["MAIL_SERVER"] = "mail.epiphane-gedeon.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
```

## 🔄 **Test Rapide**

Une fois le mot de passe configuré :

```bash
python test_smtp_prive.py
```

Si ça marche, vous verrez :
```
✅ Email de test envoyé avec succès !
```

## 📞 **Support LWS**

Si vous avez des difficultés :

- **Support LWS :** https://aide.lws.fr/
- **Panel client :** Votre espace client LWS
- **Demandez :** "Paramètres SMTP pour egpouli@epiphane-gedeon.com"

## 🎯 **Résumé des Étapes**

1. ✅ **Serveur SMTP trouvé** : `mail.epiphane-gedeon.com` (LWS)
2. ⚠️ **À faire** : Corriger le mot de passe email
3. 🧪 **Tester** : `python test_smtp_prive.py`
4. 🚀 **Lancer** : `flask run` et tester les formulaires

Une fois le mot de passe corrigé, vos emails apparaîtront comme envoyés depuis `egpouli@epiphane-gedeon.com` ! 🎉