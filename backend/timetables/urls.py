from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LessonUnitViewSet, PeriodViewSet, GroupTimeTableViewSet


router = DefaultRouter()
router.register(r'lesson_unit', LessonUnitViewSet, basename='lesson_unit')
router.register(r'period', PeriodViewSet, basename='period')
router.register(r'group_timetable', GroupTimeTableViewSet, basename='room')

urlpatterns = [
    path('', include(router.urls)),
]
