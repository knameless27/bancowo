from utils.SoftDeleteModel import SoftDeleteModel
from users.models import User
from django.db import models
import random


def create_new_number():
    return str(random.randint(1000000000, 9999999999))


class TransactionType(SoftDeleteModel, models.Model):
    name = models.CharField()
    deleted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class TransactionStatus(SoftDeleteModel, models.Model):
    name = models.CharField()
    deleted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CardType(SoftDeleteModel, models.Model):
    name = models.CharField()
    deleted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class AccountCardStatus(SoftDeleteModel, models.Model):
    name = models.CharField()
    deleted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class AccountType(SoftDeleteModel, models.Model):
    name = models.CharField()
    deleted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class AccountStatus(SoftDeleteModel, models.Model):
    name = models.CharField()
    deleted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class StatusLoan(SoftDeleteModel, models.Model):
    name = models.CharField()
    deleted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Account(SoftDeleteModel, models.Model):
    number = models.CharField(
        editable=False,
        auto_created=True,
        unique=True,
        max_length=12,
        default=create_new_number,
    )
    currency = models.CharField(max_length=3)
    account_type = models.ForeignKey(
        AccountType, related_name="type", on_delete=models.PROTECT
    )
    account_status = models.ForeignKey(
        AccountStatus, related_name="status", on_delete=models.PROTECT
    )
    user = models.ForeignKey(User, related_name="user", on_delete=models.PROTECT)
    deleted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Loan(SoftDeleteModel):
    amount = models.FloatField()
    interest_rate = models.FloatField()
    end_date = models.DateTimeField()
    account = models.ForeignKey(
        Account, related_name="loans", on_delete=models.PROTECT
    )
    status_loan = models.ForeignKey(
        StatusLoan, related_name="status", on_delete=models.PROTECT
    )
    deleted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class AccountCard(SoftDeleteModel, models.Model):
    account = models.ForeignKey(
        Account, related_name="cards", on_delete=models.PROTECT
    )
    card_type = models.ForeignKey(
        CardType, related_name="type", on_delete=models.PROTECT
    )
    account_card_status = models.ForeignKey(
        AccountCardStatus, related_name="status", on_delete=models.PROTECT
    )
    value = models.FloatField(default=0)
    deleted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Transaction(SoftDeleteModel, models.Model):
    account_card = models.ForeignKey(
        AccountCard, related_name="card", on_delete=models.PROTECT
    )
    destination_account_card = models.ForeignKey(
        AccountCard, related_name="destination_account_card", on_delete=models.PROTECT
    )
    transaction_type = models.ForeignKey(
        TransactionType, related_name="type", on_delete=models.PROTECT
    )
    transaction_status = models.ForeignKey(
        TransactionStatus, related_name="status", on_delete=models.PROTECT
    )
    description = models.TextField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
