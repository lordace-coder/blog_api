from rest_framework import serializers

from .models import Messages, Notifications

# * definition helpers
ModelSerializer = serializers.ModelSerializer
MethodField = serializers.SerializerMethodField



class NotificationSerializer(ModelSerializer):
    user = serializers.CharField(source='user.username')
    class Meta:
        model = Notifications
        fields = (
            'notification',
            'user',
            'read',
            'formated_time'
        )