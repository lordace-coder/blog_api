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
    date = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
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
            "post_detail_url",
            'date'
        ]
    def get_date(self, obj):
        return obj.get_formated_date

    def get_intro(self,obj):
        return obj.post[0:300]
    
    def get_category(self,obj:Post):
        qs = obj.category.first()
        return f"{qs}"
    def get_author(self,obj):
        return "ZenBlog"


class PostDetailSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(read_only = True,many=True)
    author = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
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
    def get_category(self,obj:Post):
        qs = obj.category.first()
        return f"{qs}"
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
    category = CategorySerializer(required=False,many=False)
    class Meta:
        model = Post
        fields = [
            "title",
            "category",
            "image",
            "post",
            "comment"
      
        ]
    
    def create(self, validated_data):
        category = validated_data.pop('category')
        new_category = Categories.objects.filter(**category)
        new_post = Post.objects.create(**validated_data)
        x= new_post
        new_post.category.set(new_category)

        new_post.save()
        return new_post
        
