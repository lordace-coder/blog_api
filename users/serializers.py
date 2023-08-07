from django.contrib.auth.models import User
from rest_framework import serializers

from .validators import validate_email


class UserSerializer(serializers.ModelSerializer):
    password= serializers.CharField(write_only=True)
    email = serializers.CharField(validators=[validate_email])
    is_staff =serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = User
        fields = ['username','email','password','is_staff']
    
    def create(self, validated_data:dict):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def get_is_staff(self,obj:User):
        return obj.is_staff