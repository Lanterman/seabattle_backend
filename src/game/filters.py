import django_filters as filters

from .models import Lobby


class LobbyFilter(filters.FilterSet):
    """Lobby filter"""

    name = filters.CharFilter(method="filter_name")
    bet = filters.RangeFilter()
    time_to_move = filters.RangeFilter()
    time_to_placement = filters.RangeFilter()
    is_private = filters.BooleanFilter(field_name="password", method="filter_is_private")

    def filter_name(self, queryset, name, value):
        return queryset.filter(name__icontains=value)

    def filter_is_private(self, queryset, name, value):
        if value == True:
            return queryset.exclude(password="")
        else:
            return queryset.filter(password="")

    class Meta:
        model = Lobby
        fields = ["name", "bet", "time_to_move", "time_to_placement", "is_private"]
