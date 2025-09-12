from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages


from blog.models import Post, Commentaire, Follow
from authentication.models import User
from . import forms, models
from blog.forms import ContactUsForm, TicketForm, ReviewForm, CommentForm, PhotoForm

@login_required()
def home(request):
    followed_users = list(Follow.objects.filter(follower=request.user).values_list('followed', flat=True))
    all_users = followed_users + [request.user.id]

    posts = Post.objects.filter(author__in=all_users).order_by('-update_at')
    return render(request, 'blog/blog.html',
                  {'posts': posts})


@login_required()
def photo_upload(request):
    form = forms.PhotoForm()
    if request.method =='POST':
        form = forms.PhotoForm(request.POST, request.FILES)
        photo = form.save(commit=False)
        photo.uploader = request.user
        photo.save()
        return redirect('home')
    return render(request, 'blog/photo_upload.html', context={'form' : form})


def comment_create(request, id):
    post = Post.objects.get(id=id)

    if request.method =='POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', id=post.id)
    else:
        form = CommentForm()

    return render(request, 'blog/post_add_comment.html',
                          {'form': form})

def comment_update(request, id):
    comment = Commentaire.objects.get(id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('post-detail', kwargs={'id': comment.post.id}))
    else:
        form = CommentForm(instance=comment)

    return render(request, 'blog/update_comment.html', {'form': form})

def comment_delete(request, id):
    comment = get_object_or_404(Commentaire, id=id)
    post_id = comment.post.id
    if comment.author != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer ce commentaire")
        
    comment.delete()
    return redirect('post-detail', id=post_id)


@login_required
def choose_post_type(request):
    return render(request, 'blog/post_creation.html')

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        photo_form = PhotoForm(request.POST, request.FILES)
        if form.is_valid() and photo_form.is_valid():
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()

            ticket = form.save(commit=False)
            ticket.author = request.user
            ticket.type = 'ticket'
            ticket.image = photo
            ticket.save()
            return redirect('post-detail', ticket.id)
    else:
        form = TicketForm()
        photo_form = PhotoForm()
    return render(request, 'blog/create_ticket.html', {'post_form': form, 'photo_form': photo_form})


@login_required
def create_review(request, ticket_id=None):
    ticket = None
    if ticket_id:
        ticket = Post.objects.get(id=ticket_id, type='ticket')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        photo_form = PhotoForm(request.POST, request.FILES)

        if form.is_valid() and photo_form.is_valid():
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()

            review = form.save(commit=False)
            review.author = request.user
            review.type = 'review'
            review.image = photo

            # ticket choisi via le champ parent_post ou passé dans l’URL
            if ticket:
                review.parent_post = ticket
            else:
                review.parent_post = form.cleaned_data.get('parent_post')

            review.save()
            return redirect('post-detail', review.id)
    else:
        form = ReviewForm(initial={'parent_post': ticket})
        photo_form = PhotoForm()

    return render(request, 'blog/create_review.html', {
        'post_form': form,
        'photo_form': photo_form,
        'ticket': ticket
    })


def post_update(request, id):
    post = get_object_or_404(Post, id=id)

    if post.author != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à modifier ce post")
    
    if post.type == 'ticket':
        post_form_class = TicketForm
    else:
        post_form_class = ReviewForm
    
    if request.method == 'POST':
        form = post_form_class(request.POST, instance=post)
        photo_instance = post.image if post.image else None
        photo_form = PhotoForm(request.POST, request.FILES, instance=photo_instance)

        if form.is_valid() and photo_form.is_valid():
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()

            updated_post = form.save(commit=False)
            updated_post.image = photo
            updated_post.save()

            return redirect('post-detail', updated_post.id)
    else:
        form = post_form_class(instance=post)
        photo_form = PhotoForm(instance=post.image)
    
    return render(request, 'blog/post_update.html', 
                  {'form': form,
                   'photo_form': photo_form
                   })


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)

    if post.author != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer ce post")
        return 

    if request.method =='POST':
        post.delete()
        return redirect('home')

    return render(request, 'blog/delete_post.html',
                  {'post': post})


def contact_us(request):
    form = ContactUsForm
    return render(request, 'blog/contact_us.html',
                  {'form': form})

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html',
                  {'posts': posts})

def post_detail(request, id):
    post = Post.objects.get(id=id)
    return render(request, 'blog/post_detail.html',
                  {'post': post})

@login_required
def profile_view(request, username): 
    user_profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user_profile).order_by('-update_at')

    is_following = Follow.objects.filter(follower=request.user, followed=user_profile).exists()

    return render(request, 'blog/profile.html', {
        'user_profile': user_profile,
        'posts': posts,
        'is_following': is_following,
    })

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if user_to_follow != request.user:
        Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
        return JsonResponse({"status": "success", "message": f"Vous suivez {user_to_follow.username}."})
    return JsonResponse({"status": "error", "message": "Action impossible."}, status=400)

@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=request.user, followed=user_to_unfollow).delete()
    return JsonResponse({"status": "success", "message": f"Vous ne suivez plus {user_to_unfollow.username}."})

@login_required
def show_following(request):
    following = request.user.following.all()
    followers = request.user.followers.all()

    return render(request, 'blog/following_list.html', {
        'following': following,
        'followers': followers,
    })
