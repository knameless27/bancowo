from users.models import User
from utils.SoftDeleteModel import SoftDeleteModel
from django.db import models


class TypeNotification(SoftDeleteModel, models.Model):
    name = models.CharField()
    deleted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

class StatusNotification(SoftDeleteModel, models.Model):
    name = models.CharField()
    deleted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(SoftDeleteModel, models.Model):
    user = models.ForeignKey(User, related_name="notifications", on_delete=models.PROTECT)
    message = models.CharField(blank=True, null=True)
    title = models.CharField(max_length=12)
    bank_name = models.CharField(null=True, max_length=360, blank=True)
    type_notification = models.ForeignKey(
        TypeNotification, related_name="type", on_delete=models.PROTECT
    )
    status_notification = models.ForeignKey(
        StatusNotification, related_name="status", on_delete=models.PROTECT
    )
    sent_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
