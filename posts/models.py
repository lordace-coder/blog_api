from django.contrib.auth import get_user_model
from django.db import models

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

    def __str__(self):
        return f"{self.author[0:10]} -{self.comment[0:20]}"


class Post(models.Model):
    title = models.TextField(max_length=100)
    post = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Categories, related_name='categories')
    comments = models.ForeignKey(Comments, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)

    def view_post(self):
        self.views += 1
        self.save()
