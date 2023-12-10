from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet, EndNoteViewSet


router = DefaultRouter()
router.register(r'note', NoteViewSet, basename='note')
router.register(r'end_note', EndNoteViewSet, basename='end_note')

urlpatterns = [
    path('', include(router.urls)),
]
