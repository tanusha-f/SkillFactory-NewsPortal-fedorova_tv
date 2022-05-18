from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from datetime import date, datetime
from django.contrib.auth.models import User
from news.models import Category, Post


def send_mail_week():
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
                subject='Новые публикации за прошедшую неделю!',
                from_email='NewsPortal <tanya-fscf@yandex.ru>',
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

