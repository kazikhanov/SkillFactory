import django_filters
from django import forms
from .models import News
from django.contrib.auth.models import User


class NewsSearchFilter(django_filters.FilterSet):
    # Поиск по названию (регистронезависимый)
    title = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={
            'placeholder': 'Поиск по названию',
            'class': 'form-control'
        }),
        label='Название'
    )

    # Поиск по имени автора
    author = django_filters.CharFilter(
        field_name='author__username',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={
            'placeholder': 'Поиск по автору',
            'class': 'form-control'
        }),
        label='Имя автора'
    )

    # Фильтр по дате (новости после указанной даты)
    pub_date = django_filters.DateFilter(
        field_name='pub_date',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label='Опубликовано после'
    )

    class Meta:
        model = News
        fields = []