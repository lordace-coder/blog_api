from datetime import timezone

from django.contrib.auth import get_user_model
from django.db import models

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

    class Meta:
        verbose_name = 'Comments'


class Post(models.Model):
    title = models.TextField(max_length=100)
    post = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to="images/posts")
    date_created = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(
        Categories, related_name='categories', blank=True, )
    comments = models.ManyToManyField(
        Comments, blank=True)
    views = models.IntegerField(default=0)

    def view_post(self):
        self.views += 1
        self.save()

    def __str__(self):
        return self.title

    @property
    def get_formated_date(self):
        return format_time_ago(self.date_created)
