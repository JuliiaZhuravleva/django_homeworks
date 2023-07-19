import django_filters

from advertisements.models import Advertisement


class AdvertisementFilter(django_filters.FilterSet):
    """Фильтры для объявлений."""
    created_at = django_filters.DateFromToRangeFilter()
    title = django_filters.CharFilter(lookup_expr='icontains')
    favourite = django_filters.BooleanFilter(method='filter_favourite')

    class Meta:
        model = Advertisement
        fields = ['creator', 'status']

    def filter_favourite(self, queryset, name, value):
        if value:
            # Если значение is_favourite равно True, вернуть только избранные объявления
            return queryset.filter(favouriteadvertisement__user=self.request.user)
        else:
            # Если значение is_favourite равно False, вернуть все объявления
            return queryset
