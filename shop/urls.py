from django.urls import path
from . import views
from .views import LikeView, DeleteItemView

urlpatterns = [
    path('delete_recomment/<int:pk>/', views.delete_recomment),
    path('update_recomment/<int:pk>/', views.ReCommentUpdate.as_view()),
    path('<int:item_pk>/<int:comment_pk>/new_recomment/', views.new_recomment, name='new_recomment'),
    path('search/<str:q>/', views.ItemSearch.as_view()),
    path('delete_comment/<int:pk>/', views.delete_comment),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),
    path('<int:pk>/new_comment/', views.new_comment),
    path('', views.ItemList.as_view(), name='item_list'),
    path('<int:pk>/', views.ItemDetail.as_view(), name='item-detail'),
    path('create_item/', views.ItemCreate.as_view()),
    path('update_item/<int:pk>/', views.ItemUpdate.as_view()),
    path('brand/<str:slug>/', views.Brand_page),
    path('category/<str:slug>/', views.Category_page),
    path('tag/<str:slug>/', views.Tag_page),
    path('like/<int:pk>', LikeView, name='likes_item'),
    path('delete_item/<int:pk>/', DeleteItemView.as_view(), name='delete_item'),
    path('favourite_item/<int:pk>/', views.favourite_item, name='favourite_item'),
    path('favourites/', views.item_favourite_list, name='item_favourite_list'),
]
