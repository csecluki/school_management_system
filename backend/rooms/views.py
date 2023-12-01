from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .filters import RoomFilter
from .models import Room
from .pagination import RoomPageNumberPagination
from .permissions import RoomPermission
from .serializers import RoomSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    pagination_class = RoomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RoomFilter
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated, RoomPermission, )
