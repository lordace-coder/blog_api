from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView,RetrieveAPIView
from rest_framework.response import Response

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



class UserProfileApiView(StaffEditOnly,RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def get(self, request, *args, **kwargs):
        obj = self.get_object()

        if not request.user.is_staff:
            return Response(status=401,data={"error":"for staff users only"})
        if request.user == obj.user or request.user.is_superuser:
           return super().get(request, *args, **kwargs)
        return Response(status=400,data={"error":"permission denied"})

    def get_object(self):
        queryset = self.get_queryset()
        user =self.request.user
        obj,created = queryset.get_or_create(user = user)

        return obj

class UserProfileVisitorsView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def get_object(self):
        name = self.kwargs.get("author")
        self.get_queryset().filter(