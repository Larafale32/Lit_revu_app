# Blog de Revue de Livres  

## Description  
Ce projet est une application web développée avec **Django**, permettant aux utilisateurs de :  
- Créer, modifier et supprimer des billets de blog (reviews de livres).  
- Ajouter et gérer des commentaires sur les billets.  
- Suivre d’autres utilisateurs pour voir leurs publications.  

L’objectif est de fournir une plateforme simple pour partager des critiques de livres et interagir avec la communauté.  

---

## Fonctionnalités principales  
- Authentification (inscription, connexion, déconnexion).  
- Gestion des billets : création, édition, suppression.  
- Gestion des commentaires : ajout, suppression.  
- Système de suivi entre utilisateurs (follow/unfollow).  
- Affichage des publications de tous les utilisateurs dans le 'flux'.  

---

## 🛠️ Installation  

### 1. Cloner le projet  
```bash
git clone https://github.com/Larafale32/Lit_revu_app
cd lit_revu_app
```
2. Créer et activer un environnement virtuel
```bash
python -m venv env
source env/bin/activate   # Mac/Linux
env\Scripts\activate      # Windows
```
3. Installer les dépendances
```bash
pip install -r requirements.txt
```
4. Appliquer les migrations
```bash
python manage.py migrate
```
5. Créer un superutilisateur (admin)
```bash
python manage.py createsuperuser
```
6. Lancer le serveur
```bash
python manage.py runserver
```

Structure du projet (simplifiée)
lit_revu_app/
│── manage.py
│── README.md
│── requirements.txt
│── db.sqlite3
│── seed.py            # script pour alimenter la base de données 
│
├── blog/              # Application principale
│   ├── models.py      # Modèles (Billets, Commentaires, Follows)
│   ├── views.py       # Vues (logique métier)
│   ├── urls.py        # Routage des pages
│   ├── templates/     # Templates HTML
│   └── static/        # Fichiers CSS/JS
│
├── authentication/    # Application pour la gestion des utilisateurs
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
    └── static/