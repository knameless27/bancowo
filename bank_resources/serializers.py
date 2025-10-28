from .models import AccountType, AccountStatus, StatusLoan, Account, Loan
from users.models import User
from rest_framework import serializers


class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = "__all__"

    def delete(self, instance):
        """
        Soft delete: marca deleted_at en lugar de eliminar físicamente.
        """
        instance.delete()
        instance.save()
        return instance


class AccountStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountStatus
        fields = "__all__"

    def delete(self, instance):
        """
        Soft delete: marca deleted_at en lugar de eliminar físicamente.
        """
        instance.delete()
        instance.save()
        return instance


class StatusLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusLoan
        fields = "__all__"

    def delete(self, instance):
        """
        Soft delete: marca deleted_at en lugar de eliminar físicamente.
        """
        instance.delete()
        instance.save()
        return instance


class AccountSerializer(serializers.ModelSerializer):
    account_type = serializers.PrimaryKeyRelatedField(queryset=AccountType.all_objects.all())
    account_status = serializers.PrimaryKeyRelatedField(queryset=AccountStatus.all_objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.all_objects.all())

    class Meta:
        model = Account
        fields = (
            "currency",
            "account_type",
            "account_status",
            "user",
            "deleted_at",
            "updated_at",
            "created_at",
        )
        read_only_fields = ("created_at", "id", "number")

    def delete(self, instance):
        """
        Soft delete: marca deleted_at en lugar de eliminar físicamente.
        """
        instance.delete()
        instance.save()
        return instance


class LoanSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    status_loan = StatusLoanSerializer()

    class Meta:
        model = Loan
        fields = "__all__"

    def delete(self, instance):
        """
        Soft delete: marca deleted_at en lugar de eliminar físicamente.
        """
        instance.delete()
        instance.save()
        return instance
