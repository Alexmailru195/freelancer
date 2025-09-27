# invoices/tasks.py
from celery import shared_task
from django.utils import timezone
from .models import Invoice

@shared_task
def update_overdue_invoices():
    today = timezone.now().date()
    updated = Invoice.objects.filter(
        due_date__lt=today,
        status='Pending'
    ).update(status='Overdue')
    return f"Обновлено {updated} просроченных счетов."