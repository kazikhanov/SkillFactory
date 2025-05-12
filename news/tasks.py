from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import News, Category


@shared_task
def notify_subscribers_new_news(news_id):
    news = News.objects.get(id=news_id)
    subscribers = news.category.subscribers.all()

    for user in subscribers:
        subject = f'Новая новость в категории {news.category.name}'
        message = render_to_string('news/weekly_news_email.html', {
            'user': user,
            'news': news,
            'domain': settings.DOMAIN,
        })

        send_mail(
            subject=subject,
            message='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=message
        )


@shared_task
def send_weekly_newsletter():
    week_ago = timezone.now() - timedelta(days=7)
    categories = Category.objects.all()

    for category in categories:
        subscribers = category.subscribers.all()
        recent_news = News.objects.filter(
            category=category,
            created_date__gte=week_ago
        )

        if recent_news.exists():
            for user in subscribers:
                subject = f'Еженедельная подборка новостей в категории {category.name}'
                message = render_to_string('news/weekly_news_email.html', {
                    'user': user,
                    'news_list': recent_news,
                    'category': category,
                    'domain': settings.DOMAIN,
                })

                send_mail(
                    subject=subject,
                    message='',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    html_message=message
                )