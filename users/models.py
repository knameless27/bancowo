from django.contrib.auth.models import AbstractUser
from utils.SoftDeleteModel import SoftDeleteModel
from django.db import models

# Create your models here.
class User(AbstractUser, SoftDeleteModel):
    last_name = models.CharField(max_length=15)
    email = models.EmailField(unique=True, max_length=150)
    phone = models.CharField(max_length=30)
    address = models.CharField(null=True, max_length=360, blank=True)
    has_multiple_owners = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Beneficiary(SoftDeleteModel, models.Model):
    user = models.ForeignKey(User, related_name="beneficiaries", on_delete=models.PROTECT)
    name = models.CharField(max_length=15)
    account_number = models.CharField(max_length=12)
    bank_name = models.CharField(null=True, max_length=360, blank=True)
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)