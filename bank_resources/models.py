from utils.SoftDeleteModel import SoftDeleteModel
from users.models import User
from django.db import models
import random


def create_new_number():
    return str(random.randint(1000000000, 9999999999))


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
        Account, related_name="account", on_delete=models.PROTECT
    )
    status_loan = models.ForeignKey(
        StatusLoan, related_name="status", on_delete=models.PROTECT
    )
    deleted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
