from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.generic import View

from . import forms


class LoginPage(View):
    template_name = 'authentication/login.html'
    form_class = forms.LoginForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)  # ✅ On passe les données POST
        message = ''
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                message = 'Identifiants invalides.'
        else:
            message = 'Formulaire invalide.'

        # ✅ Toujours retourner une réponse
        return render(request, self.template_name, context={'form': form, 'message': message})


def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                message = f'Bonjour {user.username}! Vous êtes connecté.'
            else:
                message = 'Identifiants invalides.'

    return render(request, 'login.html/login.html', context={'form':form, 'message':message})

def logout_user(request):
    logout(request)
    return redirect('')

def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', {'form': form})
