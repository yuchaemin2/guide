from django.contrib import admin
from .models import QnA, QComment, QReComment

# Register your models here.
admin.site.register(QnA)
admin.site.register(QComment)
admin.site.register(QReComment)