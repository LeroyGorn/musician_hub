from django.contrib import admin

from music.models import ForumCategory, ForumComments, ForumPosted

for model in (ForumPosted, ForumComments, ForumCategory):
    admin.site.register(model)
