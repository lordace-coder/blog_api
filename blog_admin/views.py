from django.views import generic
from posts.models import Post,Comments
from django.contrib.auth.models import User
# Create your views here.


class PostsView(generic.ListView):
    queryset = Post.objects.all()
    context_object_name = 'posts'
    template_name = ''
    