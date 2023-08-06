from django.http import Http404
from rest_framework import generics, status
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .mixins import StaffEditOnly, UserEditOnly
from .models import Categories, Comments, Post
from .serializers import (CategorySerializer, CommentSerializer,
                          PostCreateSerializer, PostDetailSerializer,
                          PostListSerializers)


@api_view(['GET'])
def index(request):
    categories = Categories.objects.all()
    data = CategorySerializer(categories,many = True)
    
    return Response(data.data)


class PostsApiView(generics.ListAPIView):
    serializer_class = PostListSerializers
    queryset = Post.objects.all()

class CreatePostView(generics.CreateAPIView, StaffEditOnly):
    serializer_class = PostCreateSerializer
    queryset = Post.objects.all()
    
    def post(self, request, *args, **kwargs):
        category = request.data.get('category')
        # for rest framework view
        if not category:
            category = request.data.get('category.category')
        image = request.data.get('image')
        if not category:
            qs = Categories.objects.get(category="Business")
        else:
            qs = Categories.objects.get(category=category)
        category_data = CategorySerializer(qs,many=False)
        new_dict ={
            'title':request.data.get('title'),
            'post':request.data.get('post'),
            'image':image if image else None,
            'category':category_data.data
        }
        serializer = self.get_serializer(data=new_dict)
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        
        return Response({'success':"post uploadedsuccesfully"})




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


class CreateComment(generics.ListCreateAPIView,UserEditOnly):
    serializer_class = CommentSerializer
    queryset = Comments.objects.all()
    authentication_classes = [TokenAuthentication]
    

    
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id')
        data = dict()
        comment = request.POST.get('comment') 
        data['comment'] = comment if comment else request.data.get('comment')
        data['author'] = request.user.username
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    
        serializer = self.get_serializer(data=data)
       
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(author=request.user)
        post.comment.add(comment)
        post.save()
    
        return Response(serializer.data, status=status.HTTP_201_CREATED)
