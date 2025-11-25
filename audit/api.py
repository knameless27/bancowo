from django_filters.rest_framework import DjangoFilterBackend
from audit.models import AuditLog
from audit.serializers import AuditLogSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ReadOnlyModelViewSet

class AuditLogViewSet(ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ["user", "entity", "status"]
    search_fields = ["action", "entity", "ip_address"]
    ordering_fields = ["created_at"]
