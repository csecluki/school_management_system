from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from users.forms import UserLoginForm, UserRegisterForm, ProfileForm
from users.models import Profile


def login_view(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.data['username'], password=form.data['password'])
            if user.is_authenticated:
                login(request, user)
                return redirect('home')
    return render(request, 'login.html', context={'form': form})


def register_view(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.create_profile()
            return redirect('create_profile')
        else:
            print(form.errors)
    return render(request, 'register.html', context={'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def profile_create_view(request):
    form = ProfileForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'profile_create.html', context={'form': form})


def profile_edit_view(request, slug):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(request.POST or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'profile.html', context={'form': form})
