from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class QnA(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'[{self.pk}]{self.title}:: {self.author}'

    def get_absolute_url(self):
        return f'/board/qna/{self.pk}/'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/1340/0b4ab25625a60211/svg/{self.author.email}'

    class Meta: #미리 지정해 놓은 몇 개의 단어를 바꾼다
        verbose_name_plural = 'QnAs'

class QComment(models.Model):
    qna = models.ForeignKey(QnA, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="qna_author")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} : {self.content}'

    def get_absolute_url(self):
        return f'{self.qna.get_absolute_url()}#qcomment-{self.pk}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/1340/0b4ab25625a60211/svg/{self.author.email}'

class QReComment(models.Model):
    comment = models.ForeignKey(QComment, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField('대댓글', max_length=150)
    updated_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta: #미리 지정해 놓은 몇 개의 단어를 바꾼다
        verbose_name_plural = 'QRecomments'

    def __str__(self):
        return f'{self.author} : {self.content}'

    def get_absolute_url(self):
        return f'{self.comment.get_absolute_url()}/#recomment-{self.pk}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/1340/0b4ab25625a60211/svg/{self.author.email}'

