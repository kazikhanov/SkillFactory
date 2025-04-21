from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import News
from datetime import datetime
from pprint import pprint


def home(request):
    return render(request, 'news/default.html')


class NewsListView(ListView):
    news = News.objects.all().order_by('-pub_date')
    model = News
    template_name = 'news/news.html'

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