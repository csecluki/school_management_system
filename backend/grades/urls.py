from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GradeViewSet, EndGradeViewSet


router = DefaultRouter()
router.register(r'grade', GradeViewSet, basename='grade')
router.register(r'end_grade', EndGradeViewSet, basename='end_grade')

urlpatterns = [
    path('', include(router.urls)),
]
