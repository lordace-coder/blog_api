from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from rest_framework import generics, pagination, status
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .mixins import StaffEditOnly, UserEditOnly
from .models import Categories, Comments, Post, ViewPost
from .pagination import StandardResultsSetPagination
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
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query and not query == ' ':
            look_up = Q(title__icontains = query)|Q(post__icontains=query)
            return super().get_queryset().filter(look_up )
        return super().get_queryset().order_by('?')


class CreatePostView( StaffEditOnly,generics.CreateAPIView):
    serializer_class = PostCreateSerializer
    queryset = Post.objects.all()

    def get(self,*args,**kwargs):
        return Response(f"{self.permission_classes}")
    def post(self, request, *args, **kwargs):
        category = request.data.get('category')
        user = request.user
        # for rest framework view
        if not category:
            category = request.data.get('category.category')
        image = request.data.get('image')
        if not category:
            qs = Categories.objects.get(category="+18")
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

        serializer.save(author = user)

        return Response({'success':"post uploaded succesfully"})




class PostDetailApiView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'




    #  todo: work on this
    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.get(slug=self.kwargs['slug'])
        user =self.request.user
        is_permitted = (obj.author == self.request.user) or self.request.user.is_superuser

        if user.is_authenticated and not ViewPost.seen(post = obj,user=user):
            obj.view_post(user=user)
        return obj





class EditDeletePostView(StaffEditOnly,generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    lookup_field = 'slug'

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.get(slug=self.kwargs['slug'])
        return obj

    def patch(self, request, *args, **kwargs):
        user:User = request.user
        obj = Post.objects.get(slug=kwargs.get('slug'))
        if obj.author == user or user.is_superuser:
            category = request.data.get('category')
            qs = Categories.objects.get(category=category)
            image =  request.data.get('image')

            category_data = CategorySerializer(qs,many=False)
            new_dict ={
                'title':request.data.get('title'),
                'post':request.data.get('post'),
                'category':category_data.data
            }
            if image:
                new_dict['image'] = image
            obj = Post.objects.get(slug=kwargs.get('slug'))
            serializer = self.get_serializer(obj,data=new_dict)
            serializer.is_valid(raise_exception=True)

            serializer.save()

            return Response({'success':"post uploaded succesfully"},status=200)
        else:
            return Response({"error":"permission denied","suggestions":"use superuser,use owner of post"},status=401)



class CreateComment(UserEditOnly,generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comments.objects.all()




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
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        category = self.kwargs.get('category')
        qs = Categories.objects.filter(category__icontains=category).first()
        new_queryset = self.queryset.filter(category=qs).order_by("?")
        return new_queryset


class TrendingPosts(generics.ListAPIView):
    serializer_class = PostListSerializers
    queryset = Post.objects.order_by('-views')


class LatestPosts(generics.ListAPIView):
    serializer_class = PostListSerializers
    queryset = Post.objects.order_by('-date_created','-views')[0:10]

def get_featured_category(request):
    category = Categories.objects.filter(category__icontains="romance").first()
    return Response(category.category)



class PostUserAction(APIView):
    queryset = Post.objects.all()
    
    def get_object(self):
        qs = self.queryset
        return qs.get(slug = self.kwargs.get('slug'))
        
    
    def get(self,*args, **kwargs):
        actions = ['like','dislike']
        user_action = kwargs.get('action')
        
        
        # check if action is valid
        if user_action in actions:
            user:User = self.request.user
            # check if user has liked post before
            if user_action == 'like':
                if self.get_object().likes.filter(id = user.id).exists():
                    return Response({'data':"user already likes post"},status=200)
                else:
                    if self.get_object().dislikes.filter(id = user.id).exists():
                        self.get_object().dislikes.remove(user)
                    self.get_object().likes.add(user)
                    return Response({'data':"post liked successfully"},status=200)
            else:
                if self.get_object().dislikes.filter(id = user.id).exists():
                    return Response({'data':"user already dislikes post"},status=200)
                else:
                    if self.get_object().likes.filter(id = user.id).exists():
                        self.get_object().likes.remove(user)
                    self.get_object().dislikes.add(user)
                    return Response({'data':"post disliked successfully"},status=200)
        return Response(status=404)