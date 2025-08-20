"""
URL configuration for merchex project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static 

import authentication.views
import blog.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # pour créer des logout views si jamais
    path('signup', authentication.views.signup_page, name='signup'),
    path('home/', blog.views.home, name='home'),
    path('contact_us/', blog.views.contact_us, name='contact-us'),
    path('posts/', blog.views.post_list, name='post_list'),
    path('posts/<int:id>', blog.views.post_detail, name='post-detail'),
    path('post/add/', blog.views.choose_post_type, name='post-create'),
    path('ticket/add/', blog.views.create_ticket, name='create-ticket'),
    path('review/add/', blog.views.create_review, name='create-review'),
    path('review/add/<int:ticket_id>/', blog.views.create_review, name='create-review-ticket'),
    path('post/<int:id>/change', blog.views.post_update, name='post-update'),
    path('post/<int:id>/delete', blog.views.post_delete, name='post-delete'),
    path('post/<int:id>/add_comment', blog.views.comment_create, name='add-comment'),
    path('comment/<int:id>/update/', blog.views.comment_update, name='update-comment'),
    path('comment/<int:id>/delete', blog.views.comment_delete, name='delete-comment'),
    path('following-list/', blog.views.show_following, name='following-list'),
    path('photo/upload/', blog.views.photo_upload, name='photo_upload'),
    path('profile/<username>/', blog.views.profile_view, name='profile'),
    
    # Url json response 
    path('follow/<username>/', blog.views.follow_user, name='follow-user'),
    path('unfollow/<username>/', blog.views.unfollow_user, name='unfollow-user'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
