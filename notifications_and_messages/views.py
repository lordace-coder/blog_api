from rest_framework import generics
from rest_framework.views import APIView

from .models import Notifications, User
from .serializers import NotificationSerializer


class NotificationApiView(generics.ListAPIView):
    queryset = Notifications.objects.all()
    serializer_class = NotificationSerializer
    
  
    def get_queryset(self):
        qs = super().get_queryset()
        username = self.kwargs.get('username')
        user = User.objects.get(username = username)
        return qs.filter(user = user)