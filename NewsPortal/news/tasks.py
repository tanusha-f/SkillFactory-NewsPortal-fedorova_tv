from celery import shared_task
from datetime import date

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from django.contrib.auth.models import User
from news.models import Post


@shared_task
def celery_notify_subscribers(pk):
    instance = Post.objects.get(pk=pk)
    subs = {}
    for category in instance.category.all():
        for sub in category.subscribers.all():
            if sub:
                if sub.username in subs.keys():
                    subs[sub.username].append(category.name)
                else:
                    subs[sub.username] = [category.name]

    for user, subsc in subs.items():
        if user != instance.author.user.username:
            categories = ', '.join(subsc)
            num = len(subsc)
            if num > 1:
                subject = f'Новая публикация в разделах "{categories}"! (from Celery)'
            else:
                subject = f'Новая публикация в разделе "{categories}"! (from Celery)'

            html_content = render_to_string(
                'email/send_new_post_cat.html',
                {'post_new': instance,
                 'cat': categories,
                 'len': num,
                 'user': user, }
            )

            msg = EmailMultiAlternatives(
                subject=subject,
                from_email='NewsPortal <tanya-fscf@yandex.ru>',
                to=[User.objects.get(username=user).email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()


@shared_task
def celery_send_mail_week():
    week = int(date.today().strftime("%V"))-1
    posts_week = Post.objects.filter(time_in__week=week)
    for user in User.objects.all():
        posts = {}
        cat_user = set(user.category_set.all().values_list('name', flat=True))
        for post in posts_week:
            post_cat = set(post.category.all().values_list('name', flat=True))
            cats = cat_user.intersection(post_cat)
            if cats:
                posts[post] = ', '.join(list(cats))

        if posts:
            html_content = render_to_string(
                'email/send_posts_cat_week.html',
                {'posts_info': posts,
                 'user': user.username, }
            )

            msg = EmailMultiAlternatives(
                subject='Новые публикации за прошедшую неделю! (from Celery)',
                from_email='NewsPortal <tanya-fscf@yandex.ru>',
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
