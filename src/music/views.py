from datetime import timedelta

from django.core.paginator import Paginator
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.views.generic.list import MultipleObjectMixin

from accounts.models import ForumUser
from music.filters import PostFilter, UserFilter
from music.forms import CommentForm
from music.models import ForumCategory, ForumComment, ForumPosted
from music.tasks import fake_data, mine_bitcoin, normalize_email_task


class IndexView(ListView):
    template_name = "index.html"
    context_object_name = "all_post"

    def get_queryset(self):
        one_month_ago = timezone.now() - timedelta(days=30)
        posts = ForumPosted.objects.filter(create_datetime__gte=one_month_ago).distinct()
        queryset = sorted([i for i in posts], key=ForumPosted.likes_count, reverse=True)
        return queryset[:4]

    def get_object(self):
        return ForumCategory.objects.get(id=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        one_month_ago = timezone.now() - timedelta(days=30)
        posts = ForumPosted.objects.filter(create_datetime__gte=one_month_ago).distinct()
        queryset = sorted([i for i in posts], key=ForumPosted.likes_count, reverse=True)
        context["top_users"] = ForumUser.objects.filter(writer__in=queryset).distinct()
        context["best_categories"] = ForumCategory.objects.all()
        return context


class PostsDetailsView(DetailView):
    template_name = "post-details.html"
    model = ForumPosted

    def get_object(self, queryset=None):
        return ForumPosted.objects.get(uuid=self.kwargs.get("uuid"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = get_object_or_404(ForumPosted, uuid=self.kwargs["uuid"])
        user = ForumUser.objects.get(writer=post)
        connected_comments = ForumComment.objects.filter(messages=post)
        number_of_comments = connected_comments.count()

        context["post"] = post
        context["user"] = user
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

        new_comment = ForumComment(
            text=text,
            author=self.request.user,
            messages=self.get_object(),
            reply_to=reply_to,
        )
        new_comment.save()
        return redirect(self.request.path_info)


class DeleteComment(DeleteView):
    template_name = "delete-comment.html"
    model = ForumComment
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            return ForumComment.objects.get(author=self.request.user, id=self.kwargs.get("pk"))
        except ForumComment.DoesNotExist:
            raise Http404("You are not allowed to delete this comment.")


class CategoryIndexView(ListView):
    template_name = "categories.html"
    model = ForumCategory
    queryset = ForumCategory.objects.all()
    context_object_name = "all_categories"
    ordering = ["-create_datetime"]
    paginate_by = 4


class CategoryListView(ListView):
    template_name = "post-categories.html"
    model = ForumPosted
    ordering = ["-create_datetime"]
    context_object_name = "post_categories"
    paginate_by = 4

    def get_object(self, queryset=None):
        return ForumCategory.objects.get(id=self.kwargs.get("pk"))

    def get_queryset(self):
        category = get_object_or_404(ForumCategory, id=self.kwargs["pk"])
        return ForumPosted.objects.filter(category=category).order_by("-create_datetime")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["category"] = super().get_queryset()
        return context


class UsersDetailsView(DetailView):
    model = ForumUser
    template_name = "users.html"
    ordering = ["-create_datetime"]

    def get_object(self, queryset=None):
        return ForumUser.objects.get(id=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = ForumPosted.objects.filter(user=super().get_object()).order_by("-create_datetime")

        context["page_obj"] = Paginator(posts, 4).get_page(self.request.GET.get("page"))
        context["most_liked"] = sorted([i for i in posts], key=ForumPosted.likes_count, reverse=True)[0]
        context["comments"] = ForumComment.objects.filter(author=super().get_object()).all().count()
        context["user"] = super().get_object()
        return context


class LikeView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        post = ForumPosted.objects.get(uuid=self.kwargs.get("uuid"))

        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)

        next_obj = request.POST.get("next", "/")
        return HttpResponseRedirect(next_obj)


class FavouritesList(ListView):
    template_name = "favourites.html"
    model = ForumPosted
    ordering = ["-create_datetime"]
    context_object_name = "posts"
    paginate_by = 4

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return ForumPosted.objects.get(uuid=self.kwargs.get("uuid"))

    def get_queryset(self):
        posts = ForumPosted.objects.filter(likes=self.request.user).all()
        comment = ForumPosted.objects.filter(thread__in=ForumComment.objects.filter(author=self.request.user)).all()
        return posts.union(comment).order_by("-create_datetime")


class CreatePost(CreateView):
    template_name = "create-post.html"
    model = ForumPosted
    fields = ["category", "image", "video", "title", "description", "content"]

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreatePost, self).form_valid(form)

    def get_success_url(self):
        return reverse("music:post", kwargs={"uuid": self.object.uuid})


class UpdatePost(UpdateView):
    template_name = "update-post.html"
    model = ForumPosted
    fields = ["image", "video", "title", "description", "content"]
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            return ForumPosted.objects.get(user=self.request.user, uuid=self.kwargs.get("uuid"))
        except ForumPosted.DoesNotExist:
            raise Http404("You are not allowed to edit this post.")


class DeletePost(DeleteView):
    template_name = "delete-post.html"
    model = ForumPosted
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            return ForumPosted.objects.get(user=self.request.user, uuid=self.kwargs.get("uuid"))
        except ForumPosted.DoesNotExist:
            raise Http404("You are not allowed to delete this post.")


class ContestIndex(ListView):
    template_name = "contests.html"
    model = ForumUser
    ordering = ["first_name"]
    context_object_name = "users"
    paginate_by = 8

    def get_object(self, queryset=None):
        return ForumUser.objects.get(id=self.kwargs.get("pk"))

    def get_queryset(self):
        return UserFilter(self.request.GET, queryset=super().get_queryset()).qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["filter"] = UserFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def querystring_url(self):
        data = self.request.GET.copy()
        data.pop(self.page_kwarg, None)
        return data.urlencode()


class PostIndex(ListView):
    template_name = "posts.html"
    model = ForumPosted
    ordering = ["-create_datetime"]
    context_object_name = "posts"
    paginate_by = 8

    def get_queryset(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset()).qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["filter"] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def querystring_url(self):
        data = self.request.GET.copy()
        data.pop(self.page_kwarg, None)
        return data.urlencode()


class RelatedPost(ListView):
    template_name = "user_posts.html"
    model = ForumPosted
    ordering = ["-create_datetime"]
    context_object_name = "posts"
    paginate_by = 4

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return ForumPosted.objects.get(uuid=self.kwargs.get("uuid"))

    def get_queryset(self):
        return ForumPosted.objects.filter(user=self.request.user).all()


def bitcoin(request):
    mine_bitcoin.delay()

    return HttpResponse("Task is started!")


def normalize_email(request):
    normalize_email_task.delay(filter=dict(email__endswith=".com"))
    return HttpResponse("Task is started")


def create_data(request):
    fake_data.delay(number=5)
    return HttpResponse("Task is started")
