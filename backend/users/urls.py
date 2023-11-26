from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProfileViewSet, TokenViewSet


router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'token', TokenViewSet, basename='token')

urlpatterns = [
    path('', include(router.urls)),
]
