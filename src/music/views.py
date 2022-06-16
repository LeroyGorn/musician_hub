from django.http import Http404
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView

from accounts.models import ForumUser
from music.models import ForumCategory, ForumComments, ForumPosted


class IndexView(ListView):
    template_name = "index.html"
    queryset = ForumPosted.objects.all()
    context_object_name = "all_post"


class PostsDetailsView(ListView):
    template_name = "contests.html"
    model = ForumPosted


class CategoryDetailsView(ListView):
    template_name = "categories.html"
    model = ForumCategory


class CommentsDetailsView(ListView):
    template_name = "contest-details.html"
    model = ForumPosted


class UsersDetailsView(ListView):
    template_name = "users.html"
    model = ForumUser
