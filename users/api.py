from .models import User
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.all_objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """
        Restaura un usuario que fue soft deleted.
        """
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"success": False, "message": "Usuario no encontrado", "data": None, "errors": None},
                status=status.HTTP_404_NOT_FOUND
            )

        if not user.deleted_at:
            return Response(
                {"success": False, "message": "El usuario ya está activo", "data": None, "errors": None},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.deleted_at = None
        user.save()
        serializer = self.get_serializer(user)
        return Response(
            {"success": True, "message": "Usuario restaurado correctamente", "data": serializer.data, "errors": None},
            status=status.HTTP_200_OK
        )
    
class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.all_objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    