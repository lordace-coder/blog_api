from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import UserSerializer


class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


@api_view(['GET'])
def user_info(request):
    print(request.user)
    if request.user.is_authenticated:
        user = UserSerializer(request.user)
        return Response(user.data)
    else:
        return Response({"error":"user object wasnt found or this user isnt authenticated"},status=404)
