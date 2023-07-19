from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления."""

    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"
    DRAFT = "DRAFT", "Черновик"


class Advertisement(models.Model):
    """Объявление."""

    title = models.TextField()
    description = models.TextField(default='')
    status = models.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.DRAFT
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} от {self.created_at}. Статус {self.status}'


class FavouriteAdvertisement(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'advertisement'], name='unique_combination')
        ]

    def clean(self):
        if self.user == self.advertisement.creator:
            raise ValidationError("Нельзя добавить свое объявление в избранное.")

    def __str__(self):
        return f'{self.user} добавил в избранное {self.advertisement}'
