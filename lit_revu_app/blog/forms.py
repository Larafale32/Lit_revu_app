from django import forms
from . import models

from blog.models import Post, Commentaire



class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ['image', 'caption']


class ContactUsForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.EmailField()
    message = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={
            'rows': 6,   # hauteur
            'cols': 50,  # largeur
            'placeholder': 'Écris ta description ici...'
        })
    )

class TicketForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description']  # image = FK vers Photo


class ReviewForm(forms.ModelForm):
    parent_post = forms.ModelChoiceField(
        queryset=Post.objects.filter(type='ticket'),
        required=False,
        label="Répond à ce ticket"
    )
    class Meta:
        model = Post
        fields = ['title', 'description', 'rating', 'parent_post']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 6, 
                'placeholder': 'Votre critique...'
            }),
        }
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['text']
