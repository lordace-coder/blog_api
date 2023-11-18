from django.apps.config import AppConfig
from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from notifications_and_messages.models import Notifications

from .models import Comments, Post

User = settings.AUTH_USER_MODEL

@receiver(post_save,sender=Post)
def handle_author_notifications(sender,instance:Post,created,*args, **kwargs):
    if created:
        notification = Notifications.objects.create(notification=f"Post {instance.title} created successfully, go view post",user=instance.author)
        notification.save()
    else:
        print(args,kwargs)
        Notifications.objects.create(notification=f"Post {instance.title} has been recently updated",user=instance.author)


@receiver(post_save,sender=Comments)
def notify_author_for_comment(sender,instance:Comments,created,*args, **kwargs):
    if created:
        post = instance.post
        notification = Notifications.objects.create(notification=f"{instance.author} commented on your story {post.title}",user=post.author)


@receiver(post_delete,sender = Comments)
def notify_user_comment_deleted(sender,instance:Comments,*args, **kwargs):
    Notifications.objects.create(notification=f"your comment was deleted for violating our policies, contact us if there was a problem",user=instance.author)


@receiver(post_delete,sender = Post)
def notify_user_comment_deleted(sender,instance:Post,*args, **kwargs):
    Notifications.objects.create(notification=f"your story was deleted by our staff for violating our policies, contact us if there was a problem",user=instance.author)