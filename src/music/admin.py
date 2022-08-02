from django.contrib import admin

from music.models import ForumCategory, ForumComment, ForumPosted

for model in (ForumPosted, ForumComment, ForumCategory):
    admin.site.register(model)
