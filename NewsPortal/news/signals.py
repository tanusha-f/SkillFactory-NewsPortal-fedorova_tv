from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .models import Post


@receiver(m2m_changed, sender=Post.category.through)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == 'post_add':
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
                    subject = f'Новая публикация в разделах "{categories}"!'
                else:
                    subject = f'Новая публикация в разделе "{categories}"!'

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
