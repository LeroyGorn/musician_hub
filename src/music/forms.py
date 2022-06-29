from django import forms
from django.db.migrations.state import get_related_models_tuples
from django.utils.translation import gettext_lazy as _

from music.models import ForumComments


class CommentForm(forms.ModelForm):
    class Meta:
        model = ForumComments

        fields = ["text", "reply_to"]

        labels = {
            "text": _(""),
        }

        widgets = {
            "content": forms.TextInput(),
        }
