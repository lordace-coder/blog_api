from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .mixins import StaffEditOnly
from .models import Comments, Post
from .serializers import (CommentSerializer, PostDetailSerializer,
                          PostListSerializers)


@api_view(['GET'])
def index(request):
    return Response('hello')


class PostsApiView(generics.ListAPIView):
    serializer_class = PostListSerializers
    queryset = Post.objects.all()

class CreatePostView(generics.CreateAPIView,StaffEditOnly):
    serializer_class = PostListSerializers
    queryset = Post.objects.all()



class PostDetailApiView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

    
    #  todo: work on this
    # def get_object(self):
    #     session = self.request.session
    #     obj = super().get_object()
    #     if 'viewed' in session:
    #         if not obj.id in session['viewed']:
    #             session['viewed'].append(obj.id)
    #             obj.view_post()
    #             session.modified = True

    #     else:
    #         session['viewed'] = list()
    #         session['viewed'].append(obj.id)
    #         obj.view_post()
    #         session.modified = True
    #     return obj


    
    
    
class EditDeletePostView(generics.RetrieveUpdateDestroyAPIView,StaffEditOnly):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class CreateComment(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comments.objects.all()

    