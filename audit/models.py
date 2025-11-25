from django.db import models
from users.models import User
from utils.SoftDeleteModel import SoftDeleteModel

class AuditLog(SoftDeleteModel, models.Model):
    ACTION_STATUS = (
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    )

    user = models.ForeignKey(
        User, related_name="audit_logs", on_delete=models.SET_NULL, null=True
    )

    action = models.CharField(max_length=255)

    entity = models.CharField(max_length=255)  # ej: "Transaction", "Account", "User"
    entity_id = models.IntegerField(null=True, blank=True)

    ip_address = models.GenericIPAddressField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=ACTION_STATUS)

    payload = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
