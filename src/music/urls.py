from django.urls import path

from music.views import (CategoryIndexView, CategoryListView, ContestIndex,
                         CreatePost, DeletePost, FavouritesList, LikeView,
                         PostIndex, PostsDetailsView, RelatedPost, UpdatePost,
                         UsersDetailsView, bitcoin, create_data,
                         normalize_email)

app_name = "music"

urlpatterns = [
    path("categories/", CategoryIndexView.as_view(), name="categories"),
    path("users/", ContestIndex.as_view(), name="users"),
    path("users/<int:pk>", UsersDetailsView.as_view(), name="user"),
    path("categories/<int:pk>", CategoryListView.as_view(), name="category"),
    path("posts/", PostIndex.as_view(), name="posts"),
    path("<uuid:uuid>/", PostsDetailsView.as_view(), name="post"),
    path("<uuid:uuid>/like/", LikeView.as_view(), name="like"),
    path("bitcoin/", bitcoin, name="bitcoin"),
    path("email/", normalize_email, name="emails"),
    path("friends/", create_data, name="friends"),
    path("create-post/", CreatePost.as_view(), name="create_post"),
    path("user-posts/", RelatedPost.as_view(), name="user_posts"),
    path("update/<uuid:uuid>/", UpdatePost.as_view(), name="update_post"),
    path("delete/<uuid:uuid>/", DeletePost.as_view(), name="delete_post"),
    path("favourites/", FavouritesList.as_view(), name="favourites"),
]
