from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.apps.config import AppConfig
from notifications_and_messages.models import Notifications

from .models import Comments, Post

User = settings.AUTH_USER_MODEL

@receiver(post_save,sender=Post)
def handle_author_notifications(sender,instance:Post,created,*args, **kwargs):
    if created:
        notification = Notifications.objects.create(notification=f"Post {instance.title} created successfully, click to view post",user=instance.author)
        notification.save()


@receiver(post_save,sender=Comments)
def notify_author_for_comment(sender,instance:Comments,created,*args, **kwargs):
    if created:
        post = instance.post
        notification = Notifications.objects.create(notification=f"{instance.author} commented on your story {post.title}",user=post.author)