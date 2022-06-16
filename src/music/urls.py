from django.urls import path

from music.views import (CategoryDetailsView, CommentsDetailsView,
                         PostsDetailsView, UsersDetailsView)

urlpatterns = [
    path("categories/", CategoryDetailsView.as_view(), name="categories"),
    path("users/", UsersDetailsView.as_view(), name="users"),
    path("contests/", PostsDetailsView.as_view(), name="posts"),
    path("contest-details/", CommentsDetailsView.as_view(), name="etc"),
]
