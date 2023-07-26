from rest_framework import serializers

from .models import Carousel, Categories, Comments, Post


class CommentSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = [
            "author",
            "comment",
            "date"
        ]

    def get_date(self, obj):
        return obj.get_formated_date


class PostListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "title",
            "views",
            "category",
            "image"
        ]


class PostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    date = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "title",
            "views",
            "category",
            "image",
            "post",
            "date",
            "comments",
        ]

    def get_date(self, obj):
        return obj.get_formated_date
