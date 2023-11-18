from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.generics import (CreateAPIView, RetrieveAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.mixins import StaffEditOnly
from users.models import UserProfile

from .serializers import UserProfileSerializer, UserSerializer


class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


@api_view(['GET'])
def user_info(request):
    if request.user.is_authenticated:
        user = UserSerializer(request.user)
        return Response(user.data)
    else:
        return Response({"error":"user object wasnt found or this user isnt authenticated"},status=404)



class UserProfileApiView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user == obj.user or request.user.is_superuser:
           return super().get(request, *args, **kwargs)
        return Response(status=400,data={"error":"permission denied"})

    def patch(self, request, *args, **kwargs):
        # * manually update email
        email = request.data.get('email')
        if email:
            user = request.user
            user.email = email
            user.save()
        return super().patch(request, *args, **kwargs)


    def get_object(self):
        queryset = self.get_queryset()
        user =self.request.user
        obj,created = queryset.get_or_create(user = user)
        return obj


class UserProfileVisitorsView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def get_object(self):
        author = self.kwargs.get("author")
        qs = self.get_queryset()
        user = User.objects.get(username = author)
        profile,_ = qs.get_or_create(user = user)
        return profile


class UserSearchView(APIView):
    serializer_class = UserSerializer

    def get(self, request):
        username = request.query_params.get("username")

        if username is None:
            raise serializers.ValidationError("Username is required.")

        users = User.objects.filter(
            Q(username__icontains=username) | Q(email__icontains=username)
        ).filter(is_staff = True)

        serializer = self.serializer_class(users, many=True)

        return Response(serializer.data)