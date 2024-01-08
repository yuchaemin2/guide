from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import os
from markdownx.models import MarkdownxField
from markdownx.utils import markdown

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/shop/tag/{self.slug}'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/shop/category/{self.slug}'

    class Meta: #미리 지정해 놓은 몇 개의 단어를 바꾼다
        verbose_name_plural = 'Categories'

class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    address = models.CharField(max_length=30, blank=True)
    contact = models.CharField(max_length=30, blank=True)
    manager = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/shop/brand/{self.slug}'

class Item(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    content = MarkdownxField()
    price = models.PositiveIntegerField(default=10000)
    color = models.CharField(max_length=30, null=True)

    head_image = models.ImageField(upload_to='shop/images/%Y/%m/%d', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    likes = models.ManyToManyField(User, related_name='item_likes', blank=True)
    favourite = models.ManyToManyField(User, related_name='favourite', blank=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    #작성자가 데이터베이스에서 삭제되었을 떄 이 포스트도 같이 삭제한다. = on_delete=models.CASCADE

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    #카테고리가 삭제된 경우 연결된 포스트까지 삭제되지 않고 해당 포스트의 카테고리 필드만 Null이 되도록.!
    brand = models.ForeignKey(Brand, null=True, blank=True, on_delete=models.SET_NULL)

    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'[{self.pk}]{self.title}:: {self.author} : {self.created_at}'

    def get_absolute_url(self):
        return f'/shop/{self.pk}/'

    def total_likes(self):
        return self.likes.count()

    def get_content_markdown(self):
        return markdown(self.content)

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/1340/0b4ab25625a60211/svg/{self.author.email}'

class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} : {self.content}'

    def get_absolute_url(self):
        return f'{self.item.get_absolute_url()}#comment-{self.pk}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/1340/0b4ab25625a60211/svg/{self.author.email}'

class ReComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField('대댓글', max_length=150)
    updated_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta: #미리 지정해 놓은 몇 개의 단어를 바꾼다
        verbose_name_plural = 'Recomments'

    def __str__(self):
        return f'{self.author} : {self.content}'

    def get_absolute_url(self):
        return f'{self.comment.get_absolute_url()}/#recomment-{self.pk}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/1340/0b4ab25625a60211/svg/{self.author.email}'
