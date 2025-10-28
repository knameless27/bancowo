from .models import Account, AccountStatus, AccountType, Loan, StatusLoan
from .serializers import (
    AccountTypeSerializer,
    AccountSerializer,
    AccountStatusSerializer,
    LoanSerializer,
    StatusLoanSerializer,
)
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response


class AccountTypeViewSet(viewsets.ModelViewSet):
    queryset = AccountType.all_objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountTypeSerializer


class AccountStatusViewSet(viewsets.ModelViewSet):
    queryset = AccountStatus.all_objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountStatusSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.all_objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountSerializer


class StatusLoanViewSet(viewsets.ModelViewSet):
    queryset = StatusLoan.all_objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StatusLoanSerializer


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.all_objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LoanSerializer
