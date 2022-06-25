from django.urls import path

from music.views import (CategoryIndexView, CategoryListView, PostsDetailsView,
                         UsersDetailsView)

app_name = "music"

urlpatterns = [
    path("categories/", CategoryIndexView.as_view(), name="categories"),
    path("users/", UsersDetailsView.as_view(), name="users"),
    path("categories/<int:pk>", CategoryListView.as_view(), name="category"),
    path("<uuid:uuid>/", PostsDetailsView.as_view(), name="post"),
    path("contests/", UsersDetailsView.as_view(), name="contests"),
]
