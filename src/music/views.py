from datetime import timedelta

from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from accounts.models import ForumUser
from music.forms import CommentForm
from music.models import ForumCategory, ForumComment, ForumPosted
from music.tasks import fake_data, mine_bitcoin, normalize_email_task


class IndexView(ListView):
    template_name = "index.html"
    one_month_ago = timezone.now() - timedelta(days=30)
    queryset = ForumPosted.objects.filter(create_datetime__gte=one_month_ago)[:5]
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
        connected_comments = ForumComment.objects.filter(messages=post)
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

        new_comment = ForumComment(
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

        next = request.POST.get("next", "/")
        return HttpResponseRedirect(next)


class FavouritesList(ListView):
    template_name = "favourites.html"
    model = ForumPosted
    ordering = ["-create_datetime"]
    paginate_by = 4

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return ForumPosted.objects.get(uuid=self.kwargs.get("uuid"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = ForumPosted.objects.filter(likes=self.request.user).all().order_by("-create_datetime")
        page = self.request.GET.get("page")
        context["posts"] = Paginator(posts, 4).get_page(page)
        return context


class CreatePost(CreateView):
    template_name = "create-post.html"
    model = ForumPosted
    fields = ["category", "image", "video", "title", "description", "content"]

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
        return ForumPosted.objects.get(user=self.request.user, uuid=self.kwargs.get("uuid"))


class DeletePost(DeleteView):
    template_name = "delete-post.html"
    model = ForumPosted
    success_url = reverse_lazy("music:users")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return ForumPosted.objects.get(user=self.request.user, uuid=self.kwargs.get("uuid"))


class ContestIndex(ListView):
    template_name = "contests.html"
    model = ForumComment


class RelatedPost(ListView):
    template_name = "user_posts.html"
    model = ForumPosted
    ordering = ["-create_datetime"]
    paginate_by = 4

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return ForumPosted.objects.get(uuid=self.kwargs.get("uuid"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = ForumPosted.objects.filter(user=self.request.user).all()
        comment = ForumPosted.objects.filter(thread__in=ForumComment.objects.filter(author=self.request.user)).all()
        page = self.request.GET.get("page")
        context["posts"] = Paginator(posts.union(comment).order_by("-create_datetime"), 4).get_page(page)
        return context


def bitcoin(request):
    mine_bitcoin.delay()

    return HttpResponse("Task is started!")


def normalize_email(request):
    normalize_email_task.delay(filter=dict(email__endswith=".com"))
    return HttpResponse("Task is started")


def create_data(request):
    fake_data.delay(number=5)
    return HttpResponse("Task is started")
