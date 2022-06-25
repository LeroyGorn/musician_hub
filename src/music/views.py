from datetime import timedelta

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import DetailView, ListView

from accounts.models import ForumUser
from music.forms import CommentForm
from music.models import ForumCategory, ForumComments, ForumPosted


class IndexView(ListView):
    template_name = "index.html"
    one_week_ago = timezone.now() - timedelta(days=7)
    queryset = ForumPosted.objects.filter(create_datetime__gte=one_week_ago)[:5]
    context_object_name = "all_post"
    # paginate_by = 4


class PostsDetailsView(DetailView):
    template_name = "post-details.html"
    model = ForumPosted

    def get_object(self, queryset=None):
        return ForumPosted.objects.get(uuid=self.kwargs.get("uuid"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uuid = self.kwargs["uuid"]

        form = CommentForm()
        post = get_object_or_404(ForumPosted, uuid=uuid)
        comments = ForumComments.objects.filter(messages=post)

        context["post"] = post
        context["comments"] = comments
        context["form"] = form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        context = super().get_context_data(**kwargs)

        post = ForumPosted.objects.filter(uuid=self.kwargs["uuid"])[0]
        comments = ForumComments.objects.filter(messages=post)

        context["post"] = post
        context["comments"] = comments
        context["form"] = form

        if form.is_valid():
            text = form.cleaned_data["text"]

            comment = ForumComments.objects.create(
                text=text,
                messages=post,
            )
            comment.save()
            form = CommentForm()
            context["form"] = form
            return self.render_to_response(context=context)

        return self.render_to_response(context=context)


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
