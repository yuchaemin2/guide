from .models import QComment, QReComment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = QComment
        exclude = ('qna', 'author', 'created_at', 'modified_at')

class ReCommentForm(forms.ModelForm):
    class Meta:
        model = QReComment
        exclude = ('comment', 'author', 'updated_at', 'modified_at')