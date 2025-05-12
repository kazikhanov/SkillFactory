from django.db import models
from datetime import datetime, timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class AuthorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    specialization = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username


class News(models.Model):
    NEWS = 'news'
    ARTICLE = 'article'
    TYPE_CHOICES = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('news-detail', kwargs={'pk': self.pk})

    def clean(self):
        today = timezone.now().date()
        user_news_today = News.objects.filter(
            author=self.author,
            created_date__date=today
        ).exclude(pk=self.pk).count()  # Исключаем текущую запись при обновлении

        if user_news_today >= 3:
            raise ValidationError('Вы не можете публиковать более 3 новостей в сутки!')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)



class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

