import django_filters

from accounts.models import ForumUser
from music.models import ForumPosted


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = ForumUser
        fields = ["first_name", "last_name"]


class PostFilter(django_filters.FilterSet):
    class Meta:
        model = ForumPosted
        fields = ["category", "user"]
