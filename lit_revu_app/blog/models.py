from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from authentication.models import User


    
class Post(models.Model):
    TICKET = 'ticket'
    REVIEW = 'review'
    TYPE_CHOICES = [
        (TICKET, 'Ticket'),
        (REVIEW, 'Critique')
    ]

    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=TICKET)
    title = models.fields.CharField(max_length=100)
    image = models.ForeignKey('Photo', null=True, blank=True, on_delete=models.SET_NULL)
    description = models.fields.CharField(max_length=1000)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    parent_post = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    def __str__(self):
        return self.title
    
    
class Photo(models.Model):
    image = models.ImageField(upload_to='images/')
    caption = models.CharField(max_length=200, blank=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    


class Commentaire(models.Model):
    text = models.fields.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE, related_name="commentaire")
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Commentaire de {self.author} sur {self.post}"

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower} suit {self.followed}"