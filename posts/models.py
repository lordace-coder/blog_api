import os
from datetime import timezone
from typing import Any, Dict, Tuple

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from helpers.format_date import format_time_ago

# Create your models here.

user = get_user_model()


class Carousel(models.Model):
    title = models.TextField(max_length=40)
    text = models.TextField(max_length=200)
    image = models.ImageField(upload_to='files/images/carousel_img')
    link = models.URLField(blank=True, null=True)


class Categories(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category



class Comments(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(user, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)

    @property
    def get_formated_date(self):
        return format_time_ago(self.date_created)

    def __str__(self):
        return f"{self.author.username[0:10]} -{self.comment[0:20]}"





class Post(models.Model):
    title = models.TextField(max_length=100)
    post = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to="images/posts")
    date_created = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(
        Categories, related_name='categories', blank=True, )

    views = models.IntegerField(default=0)
    comment = models.ManyToManyField(Comments,related_name='user_comments',blank=True,null=True)
    def view_post(self):
        self.views += 1
        self.save()

    def __str__(self):
        return self.title

    @property
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})
    
    @property
    def get_formated_date(self):
        return format_time_ago(self.date_created)
    
    def delete(self,*args, **kwargs) :
        if self.image:
            # print(dir(self.image.))
            os.remove(self.image.path)
        return super().delete(*args, **kwargs)

