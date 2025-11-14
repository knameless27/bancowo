from .models import (
    AccountCard,
    AccountCardStatus,
    AccountType,
    AccountStatus,
    CardType,
    StatusLoan,
    Account,
    Loan,
    Transaction,
    TransactionStatus,
    TransactionType,
)
from users.models import User
from rest_framework import serializers


class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = "__all__"

    def delete(self, instance):
        """
        Soft delete: marca deleted_at en lugar de eliminar físicamente.
        """
        instance.delete()
        instance.save()
        return instance


class TransactionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionStatus
        fields = "__all__"

    def delete(self, instance):
        """
        Soft delete: marca deleted_at en lugar de eliminar físicamente.
        """
        instance.delete()
        instance.save()
        return instance


class CardTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardType
        fields = "__all__"

    def delete(self, instance):
        """
        Soft delete: marca deleted_at en lugar de eliminar físicamente.
        """
        instance.delete()
        instance.save()
        return instance


class AccountCardStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountCardStatus
        fields = "__all__"

    def delete(self, instance):
        """
        Soft delete: marca deleted_at en lugar de eliminar físicamente.
        """
        instance.delete()
        instance.save()
        return instance


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
    account_type = serializers.PrimaryKeyRelatedField(
        queryset=AccountType.all_objects.all()
    )
    account_status = serializers.PrimaryKeyRelatedField(
        queryset=AccountStatus.all_objects.all()
    )
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


class AccountCardSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    card_type = serializers.PrimaryKeyRelatedField(queryset=CardType.all_objects.all())
    account_card_status = serializers.PrimaryKeyRelatedField(
        queryset=AccountCardStatus.all_objects.all()
    )

    class Meta:
        model = AccountCard
        fields = (
            "account",
            "card_type",
            "card_status",
            "value",
            "deleted_at",
            "updated_at",
            "created_at",
        )
        read_only_fields = ("created_at", "id")

    def delete(self, instance):
        """
        Soft delete: marca deleted_at en lugar de eliminar físicamente.
        """
        instance.delete()
        instance.save()
        return instance

class TransactionSerializer(serializers.ModelSerializer):
    account_card = AccountCardSerializer()
    destination_account_card = AccountCardSerializer()
    transaction_type = serializers.PrimaryKeyRelatedField(queryset=TransactionType.all_objects.all())
    transaction_status = serializers.PrimaryKeyRelatedField(
        queryset=TransactionStatus.all_objects.all()
    )

    class Meta:
        model = Transaction
        fields = (
            "account",
            "destination_account",
            "transaction_type",
            "transaction_status",
            "description",
            "deleted_at",
            "updated_at",
            "created_at",
        )
        read_only_fields = ("created_at", "id")

    def delete(self, instance):
        """
        Soft delete: marca deleted_at en lugar de eliminar físicamente.
        """
        instance.delete()
        instance.save()
        return instance