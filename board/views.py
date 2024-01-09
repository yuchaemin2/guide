from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import QnA, QComment, QReComment
from .forms import CommentForm, ReCommentForm
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

# Create your views here.
class DeleteQnAView(DeleteView):
    model = QnA
    template_name = 'board/delete_qna.html'
    success_url = reverse_lazy('qna_list')

class QnAUpdate(LoginRequiredMixin, UpdateView):
    model = QnA
    fields = ['title', 'content']

    template_name = 'board/qna_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(QnAUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

class QnAList(ListView):
    model = QnA
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(QnAList, self).get_context_data()
        context['total_comments'] = QComment.objects.count

        return context

class QnADetail(DetailView):
    model = QnA

    def get_context_data(self, **kwargs):
        context = super(QnADetail, self).get_context_data()
        context['comment_form'] = CommentForm
        context['recomment_form'] = ReCommentForm
        return context

class QnACreate(LoginRequiredMixin, CreateView):
    model = QnA
    fields = ['title', 'content']

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            response = super(QnACreate, self).form_valid(form)

            return response
        else:
            return redirect('/board/qna/')

class QnASearch(QnAList):
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        qna_list = QnA.objects.filter(
            Q(title__contains=q)
        ).distinct()
        return qna_list

    def get_context_data(self, **kwargs):
        context = super(QnASearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search : {q} ({self.get_queryset().count()})'

        return context

def new_qcomment(request, pk):
    if request.user.is_authenticated:
        qna = get_object_or_404(QnA, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.qna = qna
                comment.author = request.user
                comment.save()
                return redirect(qna.get_absolute_url())
        else:
            return redirect(qna.get_absolute_url())
    else:
        raise PermissionDenied

def delete_comment(request, pk):
    comment = get_object_or_404(QComment, pk=pk)
    qna = comment.qna
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(qna.get_absolute_url())
    else:
        raise PermissionDenied

class QCommentUpdate(LoginRequiredMixin, UpdateView):
    model = QComment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(QCommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            return PermissionDenied

def QComment_page(request, pk):
    qcomment = QComment.objects.get(pk=pk)

    return render(request, 'board/qna_list.html', {
        'qcomment': QComment.objects.all().count,
    })

def new_recomment(request, qna_pk, qcomment_pk):
    if request.user.is_authenticated:
        qna = get_object_or_404(QnA, pk=qna_pk)
        comment = get_object_or_404(QComment, pk=qcomment_pk)

        if request.method == 'POST':
            recomment_form = ReCommentForm(request.POST)
            if recomment_form.is_valid():
                recomment = recomment_form.save(commit=False)
                recomment.qna = qna
                recomment.comment = comment
                recomment.author = request.user
                recomment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(comment.get_absolute_url())
    else:
        raise PermissionDenied

class ReCommentUpdate(LoginRequiredMixin, UpdateView):
    model = QReComment
    form_class = ReCommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(ReCommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

def delete_recomment(request, pk):
    recomment = get_object_or_404(QReComment, pk=pk)
    comment = recomment.comment
    if request.user.is_authenticated and request.user == recomment.author:
        recomment.delete()
        return redirect(comment.get_absolute_url())
    else:
        raise PermissionDenied
