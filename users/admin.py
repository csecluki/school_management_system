from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.sessions.models import Session

from users.models import User, Profile

admin.site.register(Permission)
admin.site.register(Session)
admin.site.register(User)
admin.site.register(Profile)
