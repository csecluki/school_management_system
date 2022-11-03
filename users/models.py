from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from django.utils.text import slugify


class UserManager(BaseUserManager):

    def create_user(self, username, email, password):
        if not username:
            raise ValueError("Please specify username for account")
        if not email:
            raise ValueError("Please specify email for account")
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("Please check if email is correct")

        user = self.model(username=username, email=email, password=None)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=32, unique=True)
    slug = models.SlugField(max_length=32, null=False, unique=True)
    email = models.EmailField(max_length=128, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
