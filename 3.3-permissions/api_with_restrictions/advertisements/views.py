from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .filters import AdvertisementFilter
from .models import Advertisement, FavouriteAdvertisement, AdvertisementStatusChoices
from .permissions import IsOwnerOrAdmin
from .serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter

    def get_queryset(self):
        user = self.request.user
        return Advertisement.objects.filter(Q(status=AdvertisementStatusChoices.OPEN) |
                                            Q(status=AdvertisementStatusChoices.CLOSED, creator=user) |
                                            Q(status=AdvertisementStatusChoices.DRAFT, creator=user))

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return []

    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def favourite(self, request, pk=None):
        advertisement = self.get_object()
        if advertisement.creator == request.user:
            return Response(
                {"detail": "Нельзя добавить в избранное свое объявление."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.method == 'POST':
            # Добавить в избранное
            FavouriteAdvertisement.objects.get_or_create(user=request.user, advertisement=advertisement)
            return Response({"detail": "Объявление добавлено в избранное."}, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            # Удалить из избранного
            FavouriteAdvertisement.objects.filter(user=request.user, advertisement=advertisement).delete()
            return Response({"detail": "Объявление удалено из избранного."}, status=status.HTTP_204_NO_CONTENT)

        return Response({"detail": "Недопустимый HTTP-метод."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)