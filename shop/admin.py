from django.contrib import admin
from .models import Item, Brand, Category, Tag, Comment, ReComment
from markdownx.admin import MarkdownxModelAdmin

# Register your models here.
admin.site.register(Item, MarkdownxModelAdmin)

class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Brand, BrandAdmin)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Tag, TagAdmin)

admin.site.register(Comment)
admin.site.register(ReComment)
