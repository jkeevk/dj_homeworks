from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action

from django_filters.rest_framework import DjangoFilterBackend

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, Favorite
from advertisements.permissions import IsOwnerOrReadOnly
from advertisements.serializers import AdvertisementSerializer, FavoriteCreateSerializer, FavoriteDetailSerializer

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from .models import AdvertisementStatusChoices
from django.db import models


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdvertisementFilter
    permission_classes = [IsOwnerOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_queryset(self):
        """Фильтрация объявлений."""
        if self.request.user.is_anonymous:
            return Advertisement.objects.filter(status=AdvertisementStatusChoices.OPEN)
        elif self.request.user.is_staff:
            return Advertisement.objects.all()
        else:
            return Advertisement.objects.filter(
                models.Q(creator=self.request.user)
                | models.Q(status=AdvertisementStatusChoices.OPEN)
            )

    def perform_create(self, serializer):
        """Сохраняет объект с текущим пользователем как создателя."""
        serializer.save(creator=self.request.user)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsOwnerOrReadOnly()]

        return super().get_permissions()

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def add_to_favorites(self, request, pk=None):
        """Добавление объявления в избранное."""
        advertisement = self.get_object()
        if advertisement.creator == request.user:
            return Response(
                {"detail": "Вы не можете добавить своё объявление в избранное."},
                status=status.HTTP_403_FORBIDDEN,
            )
        if Favorite.objects.filter(
            advertisement=advertisement, user=request.user
        ).exists():
            return Response(
                {"detail": "Это объявление уже добавлено в избранное."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        favorite_data = {"advertisement": advertisement.id}
        serializer = FavoriteCreateSerializer(
            data=favorite_data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def list_favorites(self, request):
        """Просмотр списка избранных объявлений."""
        favorites = Favorite.objects.filter(user=request.user).select_related(
            "advertisement"
        )
        serializer = FavoriteDetailSerializer(favorites, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
