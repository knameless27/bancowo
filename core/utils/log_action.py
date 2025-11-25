from audit.models import AuditLog

def log_action(user, action, entity, entity_id=None, status="SUCCESS", payload=None, ip=None):
    AuditLog.objects.create(
        user=user,
        action=action,
        entity=entity,
        entity_id=entity_id,
        status=status,
        payload=payload,
        ip_address=ip,
    )
