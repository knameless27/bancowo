from .serializers import LoginSerializer, UserSerializer, RegisterSerializer
from rest_framework import viewsets, permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.all_objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    @action(detail=True, methods=["post"])
    def restore(self, request, pk=None):
        """
        Restaura un usuario que fue soft deleted.
        """
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"message": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        if not user.deleted_at:
            return Response(
                {"message": "El usuario ya está activo"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.deleted_at = None
        user.save()
        serializer = self.get_serializer(user)
        return Response(
            {"message": "Usuario restaurado correctamente", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.all_objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        user_data = UserSerializer(user).data

        return Response(
            {
                "message": "Usuario registrado correctamente",
                "data": {"user": user_data, "token": access},
            },
            status=status.HTTP_201_CREATED,
        )


class LoginViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]  # type: ignore
        password = serializer.validated_data["password"]  # type: ignore

        user = authenticate(request, username=username, password=password)

        if not user:
            return Response(
                {
                    "success": False,
                    "message": "Credenciales inválidas",
                    "data": None,
                    "errors": None,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        user_data = UserSerializer(user).data

        return Response(
            {
                "success": True,
                "message": "Inicio de sesión exitoso",
                "data": {"user": user_data, "token": access},
                "errors": None,
            },
            status=status.HTTP_200_OK,
        )
