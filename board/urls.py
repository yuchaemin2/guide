from django.urls import path
from . import views
from .views import DeleteQnAView

urlpatterns = [
    path('delete_recomment/<int:pk>/', views.delete_recomment),
    path('update_recomment/<int:pk>/', views.ReCommentUpdate.as_view()),
    path('<int:qna_pk>/<int:qcomment_pk>/new_recomment/', views.new_recomment, name='new_qrecomment'),

    path('delete_qna/<int:pk>/', DeleteQnAView.as_view(), name='delete_qna'),
    path('delete_comment/<int:pk>/', views.delete_comment),
    path('update_qna/<int:pk>/', views.QnAUpdate.as_view(), name='update_qna'),
    path('qna/update_comment/<int:pk>/', views.QCommentUpdate.as_view()),
    path('qna/<int:pk>/new_comment/', views.new_qcomment),
    path('qna/search/<str:q>/', views.QnASearch.as_view()),
    path('qna/create/', views.QnACreate.as_view()),
    path('qna/<int:pk>/', views.QnADetail.as_view()),
    path('qna/', views.QnAList.as_view(), name='qna_list'),
]