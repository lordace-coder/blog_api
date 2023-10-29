from collections.abc import Iterable

from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db import models

from posts.models import Post


# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.CharField(max_length = 200,null = True,blank = True)
    mobile = models.CharField(max_length=20,null = True,blank=True)
    image = CloudinaryField(blank = True,null = True)
    full_name = models.CharField(max_length = 200,null = True,blank = True)
    
    
    
    def get_posts_by_user(self):
        qs = Post.objects.filter(author = self.user)[0:11]
        if not qs.exists():
            return None
        return qs
    
    def save(self, *args, **kwargs) -> None:
        if not self.user.is_staff:
            self.user.is_staff = True
            self.user.save()
        return super().save(*args, **kwargs)