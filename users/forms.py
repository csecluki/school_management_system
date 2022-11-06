from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from users.models import User, Profile


class DateInput(forms.DateInput):
    input_type = 'date'


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):

    class Meta:
        model = User


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ('user',)
        widgets = {
            'birth_date': DateInput(),
        }
