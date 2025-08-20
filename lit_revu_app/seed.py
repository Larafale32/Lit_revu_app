import os
import django
import random
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lit_revu_app.settings')
django.setup()

from authentication.models import User
from blog.models import Post, Photo, Follow

# Supprimer les données existantes pour repartir propre
User.objects.all().delete()
Post.objects.all().delete()
Photo.objects.all().delete()
Follow.objects.all().delete()

# Créer 10 utilisateurs
users = []
for i in range(10):
    user = User.objects.create_user(
        username=f"user{i+1}",
        password="password123",
        email=f"user{i+1}@test.com"
    )
    users.append(user)

# Créer quelques relations Follow
for _ in range(15):
    follower = random.choice(users)
    followed = random.choice(users)
    if follower != followed:
        Follow.objects.get_or_create(follower=follower, followed=followed)

# Créer des photos fictives (images génériques)
photos = []
for i in range(5):
    photo = Photo.objects.create(
        image="images/test_image.jpg",  # mettre un fichier réel dans /media/images/
        caption=f"Photo {i+1}",
        uploader=random.choice(users)
    )
    photos.append(photo)

# Créer des posts (tickets + reviews)
for i in range(20):
    author = random.choice(users)
    image = random.choice(photos)
    if i % 2 == 0:
        post_type = "ticket"
        title = f"Demande critique #{i+1}"
        description = f"Description de la demande critique #{i+1}"
    else:
        post_type = "review"
        title = f"Critique de livre #{i+1}"
        description = f"Mon avis sur le livre #{i+1}"
    
    Post.objects.create(
        type=post_type,
        title=title,
        image=image,
        description=description,
        create_at=timezone.now(),
        update_at=timezone.now(),
        author=author,
        rating=random.randint(0, 5) if post_type == "review" else None
    )

print("✅ Base de données remplie avec succès !")
