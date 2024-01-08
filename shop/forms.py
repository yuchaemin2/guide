from .models import Comment, ReComment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('item', 'author', 'created_at', 'modified_at', )

class ReCommentForm(forms.ModelForm):
    class Meta:
        model = ReComment
        exclude = ('comment', 'author', 'updated_at', 'modified_at', )

