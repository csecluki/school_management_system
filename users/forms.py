from django.contrib.auth import forms

from users.models import User


class UserRegisterForm(forms.UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(forms.AuthenticationForm):

    class Meta:
        model = User
