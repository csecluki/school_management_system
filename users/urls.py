from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/create/', views.profile_create_view, name='profile_create'),
    path('profile/<str:slug>/edit', views.profile_edit_view, name='profile'),
]
