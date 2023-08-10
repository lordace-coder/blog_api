from rest_framework import serializers

from posts.models import Post


def validate_title(value):
    query = Post.objects.filter(title__iexact=value)
    if query.exists():
        raise serializers.ValidationError("Account with this email address already exists")
    if '@' not in value:
        raise serializers.ValidationError("Invalid email address")
    return value
