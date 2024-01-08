from django.urls import path
from . import views

urlpatterns = [ #IP 주소/
    path('', views.home),             #IP 주소/
    path('company/', views.company),
]