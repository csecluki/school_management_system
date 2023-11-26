from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecruitmentStrategyViewSet, GroupEnrollmentViewSet, StudentEnrollmentViewSet


router = DefaultRouter()
router.register(r'recruitment_strategy', RecruitmentStrategyViewSet, basename='recruitment_strategy')
router.register(r'group_enrollment', GroupEnrollmentViewSet, basename='group_enrollment')
router.register(r'student_enrollment', StudentEnrollmentViewSet, basename='student_enrollment')

urlpatterns = [
    path('', include(router.urls)),
]
