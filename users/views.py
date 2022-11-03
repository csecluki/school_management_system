from django.shortcuts import render, redirect

from users.forms import UserLoginForm, UserRegisterForm


def login_view(request):
    context = {'form': UserLoginForm()}
    return render(request, 'login.html', context)


def register_view(request):
    context = {'form': UserRegisterForm()}
    return render(request, 'register.html', context)


def logout_view(request):
    return redirect('..')
