from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubjectViewSet, CourseViewSet, CourseGroupViewSet


router = DefaultRouter()
router.register(r'subject', SubjectViewSet, basename='subject')
router.register(r'course', CourseViewSet, basename='course')
router.register(r'course_group', CourseGroupViewSet, basename='course_group')

urlpatterns = [
    path('', include(router.urls)),
]
