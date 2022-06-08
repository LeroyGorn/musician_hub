import uuid

from django.contrib.auth import get_user_model
from django.db import models


class ForumPosted(models.Model):
    category = models.ForeignKey(to="music.ForumCategory", related_name="posts", on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), related_name="customer", on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True, unique=True)
    image = models.ImageField(default="default.png", upload_to="media/covers")
    title = models.CharField(max_length=128, blank=True)
    description = models.CharField(max_length=2048, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def messages_count(self):
        return self.thread.count()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class ForumCategory(models.Model):
    name = models.CharField(max_length=128)
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True, unique=True)

    def __str__(self):
        return f"{self.name}"


class ForumComments(models.Model):
    author = models.ForeignKey(get_user_model(), related_name="users", on_delete=models.CASCADE)
    messages = models.ForeignKey(to="music.ForumPosted", related_name="thread", on_delete=models.CASCADE)
    text = models.CharField(max_length=2048, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.text})"


class ForumReplies(models.Model):
    writer = models.ForeignKey(get_user_model(), related_name="commentator", on_delete=models.CASCADE)
    replies = models.ForeignKey(to="music.ForumComments", related_name="comments", on_delete=models.CASCADE)
    text = models.CharField(max_length=2048, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.text})"
