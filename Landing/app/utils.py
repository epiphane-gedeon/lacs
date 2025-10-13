"""
Utilitaires pour la gestion des utilisateurs et des images
"""

import os
import uuid
import base64

try:
    from PIL import Image

    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
from app import db
from app.models import Utilisateur
from werkzeug.security import generate_password_hash
import datetime


def allowed_file(filename, allowed_extensions):
    """
    Vérifie si le fichier a une extension autorisée

    Args:
        filename (str): Nom du fichier
        allowed_extensions (set): Extensions autorisées

    Returns:
        bool: True si autorisé, False sinon
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def save_document(document_file, upload_folder="documents"):
    """
    Sauvegarde un document uploadé (PDF, images)

    Args:
        document_file: Fichier Flask
        upload_folder (str): Dossier de destination

    Returns:
        dict: {'success': bool, 'filename': str, 'error': str}
    """
    try:
        if not document_file or document_file.filename == "":
            return {"success": False, "error": "Aucun fichier sélectionné"}

        # Vérifier l'extension pour les documents
        allowed_extensions = {"pdf", "png", "jpg", "jpeg", "gif", "webp"}
        if not allowed_file(document_file.filename, allowed_extensions):
            return {"success": False, "error": "Type de fichier non autorisé"}

        # Générer un nom de fichier unique
        file_extension = document_file.filename.rsplit(".", 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"

        # Créer le dossier de destination s'il n'existe pas
        upload_path = os.path.join("app", "static", upload_folder)
        os.makedirs(upload_path, exist_ok=True)

        # Chemin complet du fichier
        file_path = os.path.join(upload_path, unique_filename)

        # Sauvegarder le document
        document_file.save(file_path)

        # Chemin relatif pour la base de données
        relative_path = f"{upload_folder}/{unique_filename}"

        return {
            "success": True,
            "filename": relative_path,
            "error": None,
        }

    except Exception as e:
        return {"success": False, "error": f"Erreur lors de la sauvegarde: {str(e)}"}


def save_image(image_file, upload_folder="images", max_size=(800, 600)):
    """
    Sauvegarde une image uploadée et la redimensionne si nécessaire

    Args:
        image_file: Fichier image Flask
        upload_folder (str): Dossier de destination
        max_size (tuple): Taille maximale (largeur, hauteur)

    Returns:
        dict: {'success': bool, 'filename': str, 'base64': str, 'error': str}
    """
    try:
        if not image_file or image_file.filename == "":
            return {"success": False, "error": "Aucun fichier sélectionné"}

        # Vérifier l'extension
        allowed_extensions = {"png", "jpg", "jpeg", "gif", "webp"}
        if not allowed_file(image_file.filename, allowed_extensions):
            return {"success": False, "error": "Type de fichier non autorisé"}

        # Générer un nom de fichier unique
        file_extension = image_file.filename.rsplit(".", 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"

        # Créer le dossier de destination s'il n'existe pas
        upload_path = os.path.join("app", "static", upload_folder)
        os.makedirs(upload_path, exist_ok=True)

        # Chemin complet du fichier
        file_path = os.path.join(upload_path, unique_filename)

        # Sauvegarder directement ou avec redimensionnement si Pillow est disponible
        if PILLOW_AVAILABLE:
            # Ouvrir et redimensionner l'image
            image = Image.open(image_file)

            # Convertir en RGB si nécessaire (pour JPEG)
            if image.mode in ("RGBA", "LA", "P"):
                image = image.convert("RGB")

            # Redimensionner si nécessaire en gardant les proportions
            image.thumbnail(max_size, Image.Resampling.LANCZOS)

            # Sauvegarder l'image
            image.save(file_path, optimize=True, quality=85)
        else:
            # Sauvegarder directement sans redimensionnement
            image_file.save(file_path)

        # Convertir en base64 pour stockage en DB (optionnel)
        with open(file_path, "rb") as img_file:
            image_base64 = base64.b64encode(img_file.read()).decode("utf-8")

        # Chemin relatif pour la base de données
        relative_path = f"{upload_folder}/{unique_filename}"

        return {
            "success": True,
            "filename": relative_path,
            "base64": image_base64,
            "error": None,
        }

    except Exception as e:
        return {"success": False, "error": f"Erreur lors de la sauvegarde: {str(e)}"}


def delete_image(image_path):
    """
    Supprime une image du système de fichiers

    Args:
        image_path (str): Chemin relatif de l'image

    Returns:
        bool: True si supprimé avec succès
    """
    try:
        if image_path:
            full_path = os.path.join("app", "static", image_path)
            if os.path.exists(full_path):
                os.remove(full_path)
                return True
    except Exception as e:
        print(f"Erreur lors de la suppression de l'image: {e}")
    return False


def create_admin():
    """
    Fonction simple pour créer un utilisateur administrateur

    Returns:
        bool: True si créé avec succès, False sinon
    """
    try:
        # Vérifier si l'admin existe déjà
        existing_admin = Utilisateur.query.filter_by(email="admin@admin.com").first()

        if existing_admin:
            print("Un utilisateur admin existe déjà.")
            return False

        # Créer le nouvel utilisateur admin
        admin_user = Utilisateur(
            nom="Equipe LACS",
            prenom="Administrateur",
            numero_telephone="0000000000",
            email="admin@admin.com",
            mot_de_passe=generate_password_hash("admin"),
            admin=True,
            created_at=datetime.datetime.today().date(),
        )

        # Sauvegarder en base
        db.session.add(admin_user)
        db.session.commit()

        print("✅ Utilisateur admin créé avec succès !")
        print("   Email: admin@admin.com")
        print("   Mot de passe: admin")

        return True

    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la création: {e}")
        return False


def get_admin_user():
    """
    Récupère l'utilisateur admin principal

    Returns:
        Utilisateur ou None
    """
    return Utilisateur.query.filter_by(email="admin@admin.com").first()


def is_admin_exists():
    """
    Vérifie si un utilisateur admin existe

    Returns:
        bool: True si existe, False sinon
    """
    return Utilisateur.query.filter_by(admin=True).first() is not None
