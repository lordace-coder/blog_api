from rest_framework import serializers

from .models import Carousel, Categories, Comments, Post
from .validators import validate_title


class CommentSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    author = serializers.CharField(source='author.username',read_only = True)
    class Meta:
        model = Comments
        exclude = ('date_created','id')

    def get_date(self, obj):
        return obj.get_formated_date



class PostListSerializers(serializers.ModelSerializer):
    # * initialize extra fields and args
    intro = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    post_detail_url = serializers.HyperlinkedIdentityField(view_name='post_detail',lookup_field='slug')
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    disliked = serializers.SerializerMethodField()
    can_update = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Post
        fields = [
            "title",
            "views",
            "category",
            "image",
            "intro",
            "author",
            "post_detail_url",
            'date',
            'slug',
            'likes_count',
            'dislikes_count',
            'can_update',
             'comment_count',
            'liked',
            'disliked',
        ]

    def get_image(self,obj):
        image = None
        if obj.image:
            image = obj.image.url
            image = str(image).replace('http','https')

        return image

    def get_date(self, obj):

        return obj.get_formated_date

    def get_intro(self,obj):
        return obj.post[0:300]

    def get_category(self,obj:Post):
        qs = obj.category.first()
        return f"{qs}"
    
    def get_author(self,obj):
        return obj.author.username
    
    def get_likes_count(self,obj):
        return obj.likes.count()

    def get_can_update(self,obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return user == obj.author or user.is_staff or user.is_admin
        return False

    def get_dislikes_count(self,obj):
        return obj.dislikes.count()

    def get_liked(self,obj:Post):
        
        user = self.context.get('request').user
        if user.is_authenticated:
            if obj.likes.contains(user):
                return True
        return False

    def get_comment_count(self,obj):
        return obj.comment.count()
    
    def get_disliked(self,obj:Post):
        user = self.context.get('request').user
        if user.is_authenticated:
            if obj.dislikes.contains(user):
                return True
        return False


class PostDetailSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(read_only = True,many=True)
    author = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField(read_only = True)
    post_detail_url = serializers.HyperlinkedIdentityField(view_name='post_detail',lookup_field='slug')
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    can_update = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            "title",
            'can_update',
            "views",
            "category",
            "image",
            "post",
            "date",
            'comment_count',
            'comment',
            'author',
            'likes_count',
            'dislikes_count',
            'post_detail_url',
            'slug'
        ]
    def get_likes_count(self,obj):
        return obj.likes.count()

    def get_can_update(self,obj):
        return self.context.get('can-update')
    
    def get_dislikes_count(self,obj):
        return obj.dislikes.count()


    def get_image(self,obj):
        image = None
        if obj.image:
            image = obj.image.url
            image = str(image).replace('http','https')
        return image

    def get_date(self, obj):
        return obj.get_formated_date

    def get_author(self,obj):
        return obj.author.username

    def get_comment_count(self,obj):
        return obj.comment.count()
    def get_category(self,obj:Post):
        qs = obj.category.first()
        return f"{qs}"



class CarouselSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Carousel
        fields = (
            "image",
            )

    def get_image(self,obj):
        image = None
        if obj.image:
            image = obj.image.url
            image = str(image).replace('http','https')
        return image

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
        new_post.category.set(new_category)

        new_post.save()
        return new_post

    def update(self, instance, validated_data):
        category = validated_data.pop('category')
        category_obj = Categories.objects.filter(**category)
        instance.category.set(category_obj)
        instance.save()
        return super().update(instance, validated_data)



class UserProfilePostListSerializers(serializers.ModelSerializer):
    intro = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            "title",
            "views",
            "category",
            "image",
            "intro",
            "author",

            'date',
            'slug'
        ]
    def get_date(self, obj):

        return obj.get_formated_date

    def get_intro(self,obj):
        return obj.post[0:300]

    def get_category(self,obj:Post):
        qs = obj.category.first()
        return f"{qs}"


