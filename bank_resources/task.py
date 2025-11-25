from celery import shared_task
from .models import AccountStatement, Transaction, AccountCard
from django.db.models import Q

@shared_task
def generate_statement_files(statement_id):
    statement = AccountStatement.objects.get(id=statement_id)

    cards = AccountCard.objects.filter(account=statement.account)

    transactions = Transaction.objects.filter(
        Q(account_card__in=cards) | Q(destination_account_card__in=cards),
        updated_at__gte=statement.start_date,
        updated_at__lte=statement.end_date,
        deleted_at__isnull=True
    )

    total_debits = 0
    total_credits = 0

    for tx in transactions:
        if tx.account_card in cards:
            total_debits += tx.account_card.value
        if tx.destination_account_card in cards:
            total_credits += tx.destination_account_card.value

    opening_balance = 0 
    closing_balance = opening_balance + total_credits - total_debits

    statement.opening_balance = opening_balance
    statement.closing_balance = closing_balance
    statement.total_debits = total_debits
    statement.total_credits = total_credits
    statement.save()

    # Aquí debes crear los archivos PDF/CSV
    # yo lo dejo así por ahora:
    statement.file_url = f"/media/statements/{statement.id}.pdf" # type: ignore
    statement.save()

    return True
