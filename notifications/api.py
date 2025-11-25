from rest_framework import viewsets, permissions
from .models import Notification, TypeNotification, StatusNotification
from .serializers import (
    NotificationSerializer,
    TypeNotificationSerializer,
    StatusNotificationSerializer,
)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Notification.objects.filter(user=user, deleted_at=None)

        notif_type = self.request.query_params.get("type")
        if notif_type:
            qs = qs.filter(type_notification_id=notif_type)

        status = self.request.query_params.get("status")
        if status:
            qs = qs.filter(status_notification_id=status)

        unread = self.request.query_params.get("unread")
        if unread == "true":
            qs = qs.filter(sent_at__isnull=True)

        return qs


class TypeNotificationViewSet(viewsets.ModelViewSet):
    queryset = TypeNotification.objects.all()
    serializer_class = TypeNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]


class StatusNotificationViewSet(viewsets.ModelViewSet):
    queryset = StatusNotification.objects.all()
    serializer_class = StatusNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
