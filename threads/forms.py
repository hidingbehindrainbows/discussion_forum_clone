from django import forms

from .models import Comment


class CommentForm(forms.ModelForm): # with Meta we're overriding the Comment model
    class Meta:
        model = Comment
        fields = ("comment","author")