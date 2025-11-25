from celery import shared_task
from django.utils import timezone
from .models import Notification
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_notification_email(notification_id):
    notification = Notification.objects.filter(id=notification_id, deleted_at=None).first()
    if not notification or not notification.user.email:
        return

    try:
        send_mail(
            subject=notification.title,
            message=notification.message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[notification.user.email],
        )
        notification.sent_at = timezone.now()
        notification.status_notification_id = 2  # Enviada
        notification.save()
    except Exception:
        notification.status_notification_id = 3  # Fallida
        notification.save()

