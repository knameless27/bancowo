import csv
from io import BytesIO
from django.http import HttpResponse
from .models import (
    Account,
    AccountCard,
    AccountCardStatus,
    AccountStatus,
    AccountType,
    CardType,
    Loan,
    StatusLoan,
    Transaction,
    TransactionStatus,
    TransactionType,
)
from .serializers import (
    AccountCardSerializer,
    AccountCardStatusSerializer,
    AccountTypeSerializer,
    AccountSerializer,
    AccountStatusSerializer,
    CardTypeSerializer,
    LoanSerializer,
    StatusLoanSerializer,
    TransactionSerializer,
    TransactionStatusSerializer,
    TransactionTypeSerializer,
)
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from typing import cast
from rest_framework.request import Request
from django.db import transaction
from reportlab.pdfgen import canvas
from django.db.models import Q
from rest_framework.response import Response


class TransactionTypeViewSet(viewsets.ModelViewSet):
    queryset = TransactionType.all_objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionTypeSerializer


class TransactionStatusViewSet(viewsets.ModelViewSet):
    queryset = TransactionStatus.all_objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionStatusSerializer


class CardTypeViewSet(viewsets.ModelViewSet):
    queryset = CardType.all_objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CardTypeSerializer


class AccountCardStatusViewSet(viewsets.ModelViewSet):
    queryset = AccountCardStatus.all_objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountCardStatusSerializer


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


class AccountCardViewSet(viewsets.ModelViewSet):
    queryset = AccountCard.all_objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountCardSerializer

    def get_queryset(self):
        user = self.request.user
        return AccountCard.objects.filter(account__user=user)

    @action(detail=True, methods=["post"])
    def withdrawal(self, request, pk=None):
        card = self.get_object()
        amount = float(request.data.get("amount", 0))

        if amount <= 0:
            return Response({"message": "Invalid amount."}, status=400)

        if card.value < amount:
            return Response({"message": "Insufficient fonds."}, status=400)

        with transaction.atomic():
            card.value -= amount
            card.save()

            tx = Transaction.objects.create(
                account_card=card,
                destination_account_card=card,
                transaction_type_id=TransactionType.objects.get(name="withdrawal").id,
                transaction_status_id=TransactionStatus.objects.get(
                    name="completed"
                ).id,
                description=f"withdrawal of {amount}",
            )

        return Response({"message": "Withdrawal successfully", "transaction_id": tx.id})

    @action(detail=True, methods=["post"])
    def send_money(self, request, pk=None):
        source_card = self.get_object()
        destination_id = request.data.get("destination_id")
        amount = float(request.data.get("amount", 0))

        if not destination_id:
            return Response({"message": "destination_id required."}, status=400)

        try:
            destination_card = AccountCard.objects.get(id=destination_id)
        except AccountCard.DoesNotExist:
            return Response(
                {"message": "doesn't exist the destination_id."}, status=404
            )

        if amount <= 0:
            return Response({"message": "invalid amount."}, status=400)

        if source_card.value < amount:
            return Response({"message": "insufficient fonds."}, status=400)

        with db_transaction.atomic():
            source_card.value -= amount
            destination_card.value += amount
            source_card.save()
            destination_card.save()

            tx = Transaction.objects.create(
                account_card=source_card,
                destination_account_card=destination_card,
                transaction_type_id=TransactionType.objects.get(name="transfer").id,
                transaction_status_id=TransactionStatus.objects.get(
                    name="completed"
                ).id,
                description=f"Transfer of {amount} to card {destination_card.id}",
            )

        return Response({"message": "Transfer successfully", "transaction_id": tx.id})


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.all_objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        request = cast(Request, self.request)
        user = request.user

        qs = Transaction.objects.filter(
            Q(account_card__account__user=user)
            | Q(destination_account_card__account__user=user)
        )

        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        min_amount = request.query_params.get("min_amount")
        max_amount = request.query_params.get("max_amount")
        status_id = request.query_params.get("status")
        type_id = request.query_params.get("type")

        if start_date:
            qs = qs.filter(created_at__date__gte=start_date)

        if end_date:
            qs = qs.filter(created_at__date__lte=end_date)

        if min_amount:
            qs = qs.filter(account_card__value__gte=min_amount)

        if max_amount:
            qs = qs.filter(account_card__value__lte=max_amount)

        if status_id:
            qs = qs.filter(transaction_status_id=status_id)

        if type_id:
            qs = qs.filter(transaction_type_id=type_id)

        return qs.order_by("-created_at")

    @action(detail=False, methods=["get"])
    def export_csv(self, request):
        transactions = self.get_queryset()

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=transactions.csv"

        writer = csv.writer(response)
        writer.writerow(["Fecha", "Origen", "Destino", "Tipo", "Estado", "Descripción"])

        for tx in transactions:
            writer.writerow(
                [
                    tx.created_at,
                    cast(AccountCard, tx.account_card).id,
                    cast(AccountCard, tx.destination_account_card).id,
                    tx.transaction_type.name,
                    tx.transaction_status.name,
                    tx.description or "",
                ]
            )

        return response

    @action(detail=False, methods=["get"])
    def export_pdf(self, request):
        transactions = self.get_queryset()

        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)

        y = 800
        pdf.setFont("Helvetica", 10)
        pdf.drawString(100, 820, "Historial de Transacciones")

        for tx in transactions:
            line = f"{tx.created_at} | {cast(AccountCard, tx.account_card).id} -> {cast(AccountCard, tx.destination_account_card).id} | {tx.transaction_type.name} | {tx.transaction_status.name}"
            pdf.drawString(50, y, line)
            y -= 20
            if y < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                y = 800

        pdf.save()
        buffer.seek(0)

        response = HttpResponse(buffer, content_type="application/pdf")
        response["Content-Disposition"] = "attachment; filename=transactions.pdf"
        return response
