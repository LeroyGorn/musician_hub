from django import forms
from django.utils.translation import gettext_lazy as _

from music.models import ForumComment


class CommentForm(forms.ModelForm):
    class Meta:
        model = ForumComment

        fields = ["text", "reply_to"]

        labels = {
            "text": _(""),
        }

        widgets = {
            "content": forms.TextInput(),
        }
