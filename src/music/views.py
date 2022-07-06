from datetime import timedelta

import pandas as pd
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import DetailView, ListView

from accounts.models import ForumUser
from music.forms import CommentForm
from music.models import ForumCategory, ForumComments, ForumPosted
from music.tasks import fake_data, mine_bitcoin, normalize_email_task

User = get_user_model()


class IndexView(ListView):
    template_name = "index.html"
    one_week_ago = timezone.now() - timedelta(days=7)
    queryset = ForumPosted.objects.filter(create_datetime__gte=one_week_ago)[:5]
    context_object_name = "all_post"


class PostsDetailsView(DetailView):
    template_name = "post-details.html"
    model = ForumPosted

    def get_object(self, queryset=None):
        return ForumPosted.objects.get(uuid=self.kwargs.get("uuid"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uuid = self.kwargs["uuid"]

        post = get_object_or_404(ForumPosted, uuid=uuid)
        connected_comments = ForumComments.objects.filter(messages=post)
        number_of_comments = connected_comments.count()

        context["post"] = post
        context["comments"] = connected_comments
        context["no_of_comments"] = number_of_comments
        context["form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(self.request.POST)
        if comment_form.is_valid():
            text = comment_form.cleaned_data["text"]
            try:
                reply_to = comment_form.cleaned_data["reply_to"]
            except ValueError:
                reply_to = None

        new_comment = ForumComments(
            text=text,
            author=self.request.user,
            messages=self.get_object(),
            reply_to=reply_to,
        )
        new_comment.save()
        return redirect(self.request.path_info)


class CategoryIndexView(ListView):
    template_name = "categories.html"
    model = ForumCategory
    queryset = ForumCategory.objects.all()
    context_object_name = "all_categories"
    ordering = ["-create_datetime"]
    paginate_by = 2


class CategoryListView(ListView):
    template_name = "post-categories.html"
    model = ForumPosted
    ordering = ["-create_datetime"]
    paginate_by = 4

    def get_object(self, queryset=None):
        return ForumCategory.objects.get(id=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_id = self.kwargs["pk"]

        category = get_object_or_404(ForumCategory, id=cat_id)
        posts = ForumPosted.objects.filter(category=category).all().order_by("-create_datetime")
        page = self.request.GET.get("page")
        context["posts"] = Paginator(posts, 4).get_page(page)
        context["category"] = category
        return context


class UsersDetailsView(ListView):
    template_name = "users.html"
    model = ForumUser


class ContestIndex(ListView):
    template_name = "contests.html"
    model = ForumComments


def bitcoin(request):
    mine_bitcoin.delay()

    return HttpResponse("Task is started!")


def normalize_email(request):
    normalize_email_task.delay(query_set=ForumUser.objects.all())
    return HttpResponse("Task is started")


def create_data(request):
    fake_data.delay(number=5)
    return HttpResponse("Task is started")
