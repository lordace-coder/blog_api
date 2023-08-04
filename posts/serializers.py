from rest_framework import serializers

from .models import Carousel, Categories, Comments, Post


class CommentSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    author = serializers.CharField(source='author.username',read_only = True)
    class Meta:
        model = Comments
        exclude = ('date_created','id')

    def get_date(self, obj):
       
        return obj.get_formated_date



class PostListSerializers(serializers.ModelSerializer):
    intro = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    post_detail_url = serializers.HyperlinkedIdentityField(view_name='post_detail',lookup_field='pk')
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "views",
            "category",
            "image",
            "intro",
            "author",
            "post_detail_url"
        ]

    def get_intro(self,obj):
        return obj.post[0:300]
    
    def get_author(self,obj):
        return "ZenBlog"


class PostDetailSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(read_only = True,many=True)
    author = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = Post
        fields = [
            "title",
            "views",
            "category",
            "image",
            "post",
            "date",
            'comment_count',
            'comment',
            'author'
        ]

    def get_date(self, obj):
        return obj.get_formated_date

    def get_author(self,obj):
        return "ZenBlog"
    
    def get_comment_count(self,obj):
        return obj.comment.count()
class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carousel
        fields = "__all__"



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = [
            'id',
            'category'
        ]


class PostCreateSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(read_only = True,many=True)
    
    class Meta:
        model = Post
        fields = [
            "title",
            "category",
            "image",
            "post",
            "comment"
      
        ]
