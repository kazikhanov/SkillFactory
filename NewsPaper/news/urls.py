from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('news/', views.NewsListView.as_view(), name='news-list'),
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news-detail')
]
