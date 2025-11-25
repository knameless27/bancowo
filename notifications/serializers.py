from rest_framework import serializers
from .models import Notification, TypeNotification, StatusNotification


class TypeNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeNotification
        fields = "__all__"


class StatusNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusNotification
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
