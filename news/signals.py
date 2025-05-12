from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail
from .models import News
from django.template.loader import render_to_string
from django.conf import settings

@receiver(post_save, sender=News)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        category = instance.category
        subscribers = category.subscribers.all()

        for user in subscribers:
            subject = f'Новая новость в категории "{category.name}"'

            message_html = render_to_string('email/notification.html', {
                'user': user,
                'news': instance,
                'category': category,
                'site_url': settings.SITE_URL,
            })

            send_mail(
                subject=subject,
                message='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=message_html,
                fail_silently=False,
            )

@receiver(post_save, sender=User)
def add_user_to_common_group(sender, instance, created, **kwargs):
    if created:
        common_group = Group.objects.get(name='common')
        instance.groups.add(common_group)

@receiver(post_save, sender=User)
def add_user_to_common_group(sender, instance, created, **kwargs):
    if created:
        common_group = Group.objects.get_or_create(name='common')[0]
        instance.groups.add(common_group)