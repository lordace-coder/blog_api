from django.http import Http404
from rest_framework import generics, status
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .mixins import StaffEditOnly, UserEditOnly
from .models import Categories, Comments, Post, ViewPost
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
    queryset = Post.objects.all().order_by('?')

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
    lookup_field = 'slug'



    
    #  todo: work on this
    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.get(slug=self.kwargs['slug'])
        user =self.request.user
        if user.is_authenticated and not ViewPost.seen(post = obj,user=user):
            obj.view_post(user=user)           
        return obj   


    
    
    
class EditDeletePostView(generics.RetrieveUpdateDestroyAPIView,StaffEditOnly):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.get(slug=self.kwargs['slug'])
        return obj



class CreateComment(generics.ListCreateAPIView,UserEditOnly):
    serializer_class = CommentSerializer
    queryset = Comments.objects.all()
    authentication_classes = [TokenAuthentication]
    

    
    def post(self, request, *args, **kwargs):
        post_slug = kwargs.get('slug')
        data = dict()
        comment = request.POST.get('comment') 
        data['comment'] = comment if comment else request.data.get('comment')
        data['author'] = request.user.username
        try:
            post = Post.objects.get(slug=post_slug)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    
        serializer = self.get_serializer(data=data)
       
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(author=request.user)
        post.comment.add(comment)
        post.save()
    
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class GetPostBycategory(generics.ListAPIView):
    serializer_class = PostListSerializers
    queryset = Post.objects.all()


    def get_queryset(self):
        category = self.kwargs.get('category')
        qs = Categories.objects.filter(category__icontains=category).first()
        new_queryset = self.queryset.filter(category=qs)
        return new_queryset


class TrendingPosts(generics.ListAPIView):
    serializer_class = PostListSerializers
    queryset = Post.objects.order_by('-views')[0:5]


class LatestPosts(generics.ListAPIView):
    serializer_class = PostListSerializers
    queryset = Post.objects.order_by('-date_created','-views')[0:10]