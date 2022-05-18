from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post
from .tasks import celery_notify_subscribers


@receiver(m2m_changed, sender=Post.category.through)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == 'post_add':
        celery_notify_subscribers.delay(instance.pk)
