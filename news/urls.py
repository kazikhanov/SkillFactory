from django.urls import path
from . import views
from .views import (
    NewsCreateView, NewsUpdateView, NewsDeleteView,
    ArticleCreateView, ArticleUpdateView, ArticleDeleteView
)
from .views import subscribe, unsubscribe
from .views import become_author


urlpatterns = [
    path('', views.home),
    path('news/', views.NewsListView.as_view(), name='news-list'),
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news-detail'),
    path('news/search/', views.NewsSearchView.as_view(), name='news-search'),
    path('news/create/', NewsCreateView.as_view(), name='news-create'),
    path('news/<int:pk>/edit/', NewsUpdateView.as_view(), name='news-edit'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news-delete'),

    path('articles/create/', ArticleCreateView.as_view(), name='article-create'),
    path('articles/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article-edit'),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article-delete'),


    path('become-author/', become_author, name='become_author'),
    # path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    # path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('category/<int:category_id>/subscribe/', subscribe, name='subscribe'),
    path('category/<int:category_id>/unsubscribe/', unsubscribe, name='unsubscribe'),
]
