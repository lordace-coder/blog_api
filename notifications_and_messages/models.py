from django.contrib.auth.models import User
from django.db import models

from helpers.format_date import format_time_ago


# Create your models here.
class Notifications(models.Model):
    notification = models.TextField()
    created_at = models.DateTimeField(auto_now_add= True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    
    @property
    def formated_time(self):
        return format_time_ago(self.created_at)


class Messages(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    reciever = models.ForeignKey(User,on_delete=models.CASCADE,related_name="reciever")
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
