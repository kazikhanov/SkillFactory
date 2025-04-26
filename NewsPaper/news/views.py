from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import News
from datetime import datetime
from pprint import pprint
from .filters import NewsSearchFilter
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import NewsForm, ArticleForm

def home(request):
    return render(request, 'news/default.html')


class NewsListView(ListView):
    news = News.objects.all().order_by('-pub_date')
    model = News
    template_name = 'news/news.html'
    paginate_by = 1
    context_object_name = 'news'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        context['lenght'] = News.objects.count()
        pprint(context)
        return context


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/detail.html'
    context_object_name = 'news'


class NewsSearchView(ListView):
    model = News
    template_name = 'news/search.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsSearchFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs.order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreateView(LoginRequiredMixin, CreateView):
    model = News
    form_class = NewsForm
    template_name = 'news/content_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.type = News.NEWS
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('news-detail', kwargs={'pk': self.object.pk})


class NewsUpdateView(LoginRequiredMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'news/content_form.html'

    def get_queryset(self):
        return super().get_queryset().filter(type=News.NEWS)

    def get_success_url(self):
        return reverse_lazy('news-detail', kwargs={'pk': self.object.pk})


class NewsDeleteView(LoginRequiredMixin, DeleteView):
    model = News
    template_name = 'news/content_confirm_delete.html'
    success_url = reverse_lazy('news-list')

    def get_queryset(self):
        return super().get_queryset().filter(type=News.NEWS)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = News
    form_class = ArticleForm
    template_name = 'news/content_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('news-detail', kwargs={'pk': self.object.pk})


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = News
    form_class = ArticleForm
    template_name = 'news/content_form.html'

    def get_queryset(self):
        return super().get_queryset().filter(type=News.ARTICLE)

    def get_success_url(self):
        return reverse_lazy('news-detail', kwargs={'pk': self.object.pk})


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = News
    template_name = 'news/content_confirm_delete.html'
    success_url = reverse_lazy('news-list')

    def get_queryset(self):
        return super().get_queryset().filter(type=News.ARTICLE)