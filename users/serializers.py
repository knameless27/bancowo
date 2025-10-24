from rest_framework import serializers
from .models import User
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ('created_at', 'id')
        extra_kwargs = {
            'password': {'write_only': True},  # no se muestra en GET
        }

    def create(self, validated_data):
        """
        Crear un usuario hasheando la contraseña automáticamente.
        """
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Actualiza un usuario. Si se pasa password, se hashea automáticamente.
        """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    def delete(self, instance):
        """
        Soft delete: marca deleted_at en lugar de eliminar físicamente.
        """
        instance.delete()
        instance.save()
        return instance

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ('created_at', 'id', "groups", "user_permissions")
        extra_kwargs = {
            'password': {'write_only': True},  # no se muestra en GET
        }

    def create(self, validated_data):
        """
        Crea un nuevo usuario y devuelve los tokens JWT.
        """
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()

        # Generar tokens JWT
        token = Token.objects.create(user=user)

        return {
            'user': user,
            "token": token.key
        }   
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},  # no se muestra en GET
        }