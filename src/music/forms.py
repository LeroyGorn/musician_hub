from django import forms

from music.models import ForumComments


class CommentForm(forms.ModelForm):
    class Meta:
        model = ForumComments
        fields = ("text",)
