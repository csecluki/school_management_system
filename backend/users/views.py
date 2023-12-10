from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .filters import UserFilter, ProfileFilter
from .models import Profile
from .serializers import UserSerializer, TokenSerializer, ProfileSerializer
# from .permissions import UserPermission, TokenPermission, ProfilePermission
# from .pagination import UserPageNumberPagination, ProfilePageNumberPagination


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
    # pagination_class = UserPageNumberPagination
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated, UserPermission, ]

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()

    def perform_create(self, serializer):
        user = serializer.save()
        students_group = get_object_or_404(Group, name='Students')
        user.groups.add(students_group)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False)
    def teacher(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        teacher_group = get_object_or_404(Group, name='Teachers')
        user.groups.add(teacher_group)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False)
    def staff(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_staff = True
        user.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(data=self.get_serializer(instance).data, status=status.HTTP_200_OK)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProfileFilter
    # pagination_class = UserPageNumberPagination
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated, UserPermission, ]


class TokenViewSet(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    # permission_classes = [TokenPermission, AllowAny, ]

    def create(self, request, *args, **kwargs):
        user = get_object_or_404(User, email=request.data['email'])
        if not user.check_password(request.data['password']):
            return Response(data={'error': "Invalid credentials. "}, status=status.HTTP_404_NOT_FOUND)
        instance, created = Token.objects.get_or_create(user=user)
        response_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        serializer = self.get_serializer(instance)
        return Response(data=serializer.data, status=response_status)
