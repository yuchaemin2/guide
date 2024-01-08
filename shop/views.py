from json import JSONDecodeError

from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views import View

from board.models import QComment, QReComment
from . import forms
from .models import Item, Brand, Category, Tag, Comment, ReComment
from .forms import CommentForm, ReCommentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from django.db.models import Q

from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy

from rest_framework import viewsets
from .serializers import itemSerializer

# Create your views here.
class itemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = itemSerializer

def item_favourite_list(request):
    user = request.user
    favourite_items = user.favourite.all()
    comment_form = Comment.objects.all()
    board_comment = QComment.objects.all()
    recomment_form = ReComment.objects.all()
    recomment_count = ReComment.objects.count()
    qrecomment_form = QReComment.objects.all()
    qrecomment_count = QReComment.objects.count()
    context = {
        'favourite_items': favourite_items,
        'comment_form': comment_form,
        'board_comment': board_comment,
        'recomment_form': recomment_form,
        'recomment_count': recomment_count,
        'qrecomment_form': qrecomment_form,
        'qrecomment_count': qrecomment_count,
    }
    return render(request, 'shop/item_favourite_list.html', context)

def favourite_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    favourite = False
    if item.favourite.filter(id=request.user.id).exists():
        item.favourite.remove(request.user)
        favourite = False
    else:
        item.favourite.add(request.user)
        favourite = True

    return HttpResponseRedirect(item.get_absolute_url())

def LikeView(request, pk):
    item = get_object_or_404(Item, pk=pk)
    liked = False
    if item.likes.filter(id=request.user.id).exists():
        item.likes.remove(request.user)
        liked = False
    else:
        item.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('item-detail', args=[str(pk)]))

class DeleteItemView(DeleteView):
    model = Item
    template_name = 'shop/delete_item.html'
    success_url = reverse_lazy('item_list')

class ItemUpdate(LoginRequiredMixin, UpdateView):
    model = Item
    fields = ['title', 'hook_text', 'content', 'price', 'color', 'head_image', 'brand', 'category']

    template_name = 'shop/item_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
            return super(ItemUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        response = super(ItemUpdate, self).form_valid(form)
        self.object.tags.clear()
        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(',', ';')
            tags_list = tags_str.split(';')
            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)
        return response

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = ';'.join(tags_str_list)
        context['categories'] = Category.objects.all() #templates를 위한 변수
        context['no_category_item_count'] = Item.objects.filter(category=None).count
        context['brands'] = Brand.objects.all()
        context['no_brand_item_count'] = Item.objects.filter(brand=None).count
        return context

class ItemCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Item
    fields = ['title', 'hook_text', 'content', 'price', 'color', 'head_image', 'brand', 'category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_superuser or current_user.is_staff):
            form.instance.author = current_user
            response = super(ItemCreate, self).form_valid(form)

            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()
                tags_str = tags_str.replace(',', ';')
                tags_list = tags_str.split(';')

                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return response
        else:
            return redirect('/shop/')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CreateView, self).get_context_data()
        context['categories'] = Category.objects.all()  # templates를 위한 변수
        context['no_category_item_count'] = Item.objects.filter(category=None).count
        context['brands'] = Brand.objects.all()
        context['no_brand_item_count'] = Item.objects.filter(brand=None).count
        return context

class ItemList(ListView):
    model = Item
    ordering = '-pk'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemList, self).get_context_data()
        context['categories'] = Category.objects.all()  # templates를 위한 변수
        context['no_category_item_count'] = Item.objects.filter(category=None).count
        context['brands'] = Brand.objects.all()
        context['no_brand_item_count'] = Item.objects.filter(brand=None).count
        return context

class ItemDetail(DetailView):
    model = Item

    def get_context_data(self, **kwargs):
        context = super(ItemDetail, self).get_context_data()
        stuff = get_object_or_404(Item, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        is_favourite = False
        if stuff.favourite.filter(id=self.request.user.id).exists():
            is_favourite = True

        context['categories'] = Category.objects.all()  # templates를 위한 변수
        context['no_category_item_count'] = Item.objects.filter(category=None).count
        context['brands'] = Brand.objects.all()
        context['no_brand_item_count'] = Item.objects.filter(brand=None).count
        context['comment_form'] = CommentForm
        context['recomment_form'] = ReCommentForm
        context['total_likes'] = total_likes
        context['liked'] = liked
        context['is_favourite'] = is_favourite
        return context

def Brand_page(request, slug):
    if slug == 'no_brand':
        brand = '미분류'
        item_list = Item.objects.filter(brand=None)
    else:
        brand = Brand.objects.get(slug=slug)
        item_list = Item.objects.filter(brand=brand)
    return render(request, 'shop/item_list.html', {
        'brand': brand,
        'item_list': item_list,
        'brands': Brand.objects.all(),
        'no_brand_item_count': Item.objects.filter(brand=None).count,
        'categories': Category.objects.all(),
        'no_category_item_count': Item.objects.filter(category=None).count
    })

def Category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        item_list = Item.objects.filter(brand=None)
    else:
        category = Category.objects.get(slug=slug)
        item_list = Item.objects.filter(category=category)
    return render(request, 'shop/item_list.html', {
        'category': category,
        'item_list': item_list,
        'brands': Brand.objects.all(),
        'no_brand_item_count': Item.objects.filter(brand=None).count,
        'categories': Category.objects.all(),
        'no_category_item_count': Item.objects.filter(category=None).count
    })

def Tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    item_list = tag.item_set.all()
    return render(request, 'shop/item_list.html', {
        'tag': tag,
        'item_list': item_list,
        'brands': Brand.objects.all(),
        'no_brand_item_count': Item.objects.filter(brand=None).count,
        'categories': Category.objects.all(),
        'no_category_item_count': Item.objects.filter(category=None).count
    })

def new_comment(request, pk):
    if request.user.is_authenticated:
        item = get_object_or_404(Item, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.item = item
                comment.author = request.user
                comment.save()
                return redirect(item.get_absolute_url())
        else:
            return redirect(item.get_absolute_url())
    else:
        raise PermissionDenied

class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    item = comment.item
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(item.get_absolute_url())
    else:
        raise PermissionDenied

class ItemSearch(ItemList):
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        item_list = Item.objects.filter(
            Q(title__contains=q) | Q(tags__name__contains=q)
        ).distinct()
        return item_list

    def get_context_data(self, **kwargs):
        context = super(ItemSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search : {q} ({self.get_queryset().count()})'

        return context

def new_recomment(request, item_pk, comment_pk):
    if request.user.is_authenticated:
        item = get_object_or_404(Item, pk=item_pk)
        comment = get_object_or_404(Comment, pk=comment_pk)

        if request.method == 'POST':
            recomment_form = ReCommentForm(request.POST)
            if recomment_form.is_valid():
                recomment = recomment_form.save(commit=False)
                recomment.item = item
                recomment.comment = comment
                recomment.author = request.user
                recomment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(comment.get_absolute_url())
    else:
        raise PermissionDenied

class ReCommentUpdate(LoginRequiredMixin, UpdateView):
    model = ReComment
    form_class = ReCommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(ReCommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

def delete_recomment(request, pk):
    recomment = get_object_or_404(ReComment, pk=pk)
    comment = recomment.comment
    if request.user.is_authenticated and request.user == recomment.author:
        recomment.delete()
        return redirect(comment.get_absolute_url())
    else:
        raise PermissionDenied


