from rest_framework import generics
from rest_framework.views import APIView

from .models import Notifications, User
from .serializers import NotificationSerializer


class NotificationApiView(generics.ListAPIView):
    queryset = Notifications.objects.all()
    serializer_class = NotificationSerializer
    
  
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        return qs.filter(user = user).order_by('-created_at').order_by('read')