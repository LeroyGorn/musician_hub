from django.urls import path

from music.views import (CategoryIndexView, CategoryListView, LikeView,
                         PostsDetailsView, UsersDetailsView, bitcoin,
                         create_data, normalize_email)

app_name = "music"

urlpatterns = [
    path("categories/", CategoryIndexView.as_view(), name="categories"),
    path("users/", UsersDetailsView.as_view(), name="users"),
    path("categories/<int:pk>", CategoryListView.as_view(), name="category"),
    path("<uuid:uuid>/", PostsDetailsView.as_view(), name="post"),
    path("contests/", UsersDetailsView.as_view(), name="contests"),
    path("<uuid:uuid>/like/", LikeView.as_view(), name="like"),
    path("bitcoin/", bitcoin, name="bitcoin"),
    path("email/", normalize_email, name="emails"),
    path("friends/", create_data, name="friends"),
]
