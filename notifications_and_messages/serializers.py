from rest_framework import serializers

from .models import Messages, Notifications

# * definition helpers
ModelSerializer = serializers.ModelSerializer
MethodField = serializers.SerializerMethodField



class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notifications
        fields = "__all__"