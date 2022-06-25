import uuid

from django.contrib.auth import get_user_model
from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    ordering = ["-create_datetime"]
    create_datetime = models.DateTimeField(null=True, auto_now_add=True)
    last_update = models.DateTimeField(null=True, auto_now=True)


class ForumPosted(BaseModel):
    category = models.ForeignKey(to="music.ForumCategory", related_name="posts", on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), related_name="writer", null=True, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True, unique=True)
    image = models.ImageField(default="default.png", upload_to="covers/")
    title = models.CharField(max_length=128, blank=True)
    description = models.CharField(max_length=128, blank=True)
    content = models.TextField(blank=True)
    likes = models.ManyToManyField(get_user_model(), blank=True, related_name="likes")

    def messages_count(self):
        return self.thread.count()

    @property
    def like_count(self):
        return self.likes.all().count()


class ForumCategory(BaseModel):
    name = models.CharField(max_length=128)
    image = models.ImageField(default="default.png", upload_to="covers/")
    description = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name}"

    def post_count(self):
        return self.posts.count()


class ForumComments(BaseModel):
    author = models.ForeignKey(get_user_model(), related_name="users", null=True, on_delete=models.CASCADE)
    messages = models.ForeignKey(to="music.ForumPosted", related_name="thread", on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    reply_to = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")

    def __str__(self):
        return f"{self.author}:{self.text}"
