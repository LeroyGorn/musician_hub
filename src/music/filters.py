import django_filters

from accounts.models import ForumUser
from music.models import ForumPosted


class UserFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr="icontains")
    last_name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = ForumUser
        fields = ["first_name", "last_name"]


class PostFilter(django_filters.FilterSet):

    CHOICES = (("old", "Older"), ("recent", "Recent"))

    ordering = django_filters.ChoiceFilter(label="Ordering", choices=CHOICES, method="filter_by_order")
    title = django_filters.CharFilter(lookup_expr="icontains")
    description = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = ForumPosted
        fields = ["category", "title", "description"]

    def filter_by_order(self, queryset, name, value):
        if value == "old":
            expression = "create_datetime"
        else:
            expression = "-create_datetime"

        return queryset.order_by(expression)
