from django.contrib.auth.models import User
from rest_framework import serializers

from .validators import validate_email


class UserSerializer(serializers.ModelSerializer):
    password= serializers.CharField(write_only=True)
    email = serializers.CharField(validators=[validate_email])
    class Meta:
        model = User
        fields = ['username','email','password']