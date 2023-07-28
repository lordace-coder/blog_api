from rest_framework import serializers

from .models import Carousel, Categories, Comments, Post


class CommentSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = "__all__"

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
    # comment =  serializers.SerializerMethodField()
    coms = serializers.CharField(source="comment.all")
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
            # 'comment',
            'coms'
        ]

    def get_date(self, obj):
        return obj.get_formated_date

    # def get_comment(self,obj):
    #     query = obj.comment.all()
    #     for i in query:
    #         print(i.author)
    #     print(dir(query))
        
    #     data =  CommentSerializer(instance=query.iterator).data
    #     print(data)
    #     return data

class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carousel
        fields = "__all__"


