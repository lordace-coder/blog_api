from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications_and_messages.models import Notifications, Reports, User
from notifications_and_messages.serializers import NotificationSerializer
from posts.mixins import StaffEditOnly
from posts.models import Post
from posts.serializers import PostDetailSerializer


class SendNotification(CreateAPIView):
    """
    send handwriten notifications to users
    """
    serializer_class = [NotificationSerializer]
    queryset  = Notifications.objects.all()
    
    def perform_create(self, serializer:NotificationSerializer):
        print(serializer,serializer.data)
        return super().perform_create(serializer)



class Announcement(StaffEditOnly,APIView):
    def post(self,request,*args, **kwargs):
        try:
            msg = request.POST.get('message')
            users = User.objects.all()
            for user in users:
                Notifications.objects.create(notification = msg,user=user)
                
            return Response('send succesfully',status=201)
        except Exception as e:
            return Response('internal server error '+str(e),status=500)



class Dashboard(StaffEditOnly,APIView):
    def get(self,request,*args, **kwargs):
        data = {
            'total-users': User.objects.all().count(),
            'posts': Post.objects.all().count(),
            'reports':Reports.objects.all().count(),
        }
        return Response(data)



# ! VIEWS FOR ADMIN ONLY
