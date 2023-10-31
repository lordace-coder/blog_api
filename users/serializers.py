from django.contrib.auth.models import User
from rest_framework import serializers

from posts.serializers import UserProfilePostListSerializers

from .models import UserProfile
from .validators import validate_email


class UserSerializer(serializers.ModelSerializer):
    password= serializers.CharField(write_only=True)
    email = serializers.CharField(validators=[validate_email])
    is_staff =serializers.SerializerMethodField(read_only = True)
    is_admin =serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = User
        fields = ['username','email','password','is_staff',"is_admin"]

    def create(self, validated_data:dict):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def get_is_staff(self,obj:User):
        return obj.is_staff

    def get_is_admin(self,obj):
        return obj.is_superuser



class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source = 'user.username',read_only=True)
    email = serializers.CharField(source = 'user.email',read_only=True)
    posts = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()
    perc_posts = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = (
            "username",
            "full_name",
            "image",
            "mobile",
            "address",
            "posts",
            "email",
            "post_count",
            "perc_posts",
        )
    def get_image(self,obj):
        image = None
        if obj.image:
            image = obj.image.url
            image = str(image).replace('http','https')

        return image
    def get_post_count(self,obj):
        count = 0
        posts = obj.get_posts_by_user()
        if not posts:
            return count
        count= posts.count()
        return count

    def get_perc_posts(self,obj):
        count = 0
        posts = obj.get_posts_by_user()
        if not posts:
            return count
        count= posts.count()
        perc = (count/150) *100
        return perc
    def get_posts(self,obj):
        posts = obj.get_posts_by_user()
        return  UserProfilePostListSerializers(posts,many=True).data