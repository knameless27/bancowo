from django.db import models

class Notification(models.Model):
    action = models.CharField()
    entity = models.CharField()
    entity_id = models.CharField()
    ip_address = models.CharField()
