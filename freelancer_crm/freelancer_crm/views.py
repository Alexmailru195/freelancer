from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from clients.models import Client
from projects.models import Project
from invoices.models import Invoice
from datetime import date

@login_required
def dashboard(request):
    user = request.user
    clients_count = Client.objects.filter(user=user).count()
    projects_count = Project.objects.filter(user=user).count()
    invoices_pending = Invoice.objects.filter(user=user, status='Pending').count()
    invoices_paid = Invoice.objects.filter(user=user, status='Paid').count()
    overdue_invoices = Invoice.objects.filter(
        user=user,
        due_date__lt=date.today(),
        status='Pending'
    ).count()

    return render(request, 'dashboard.html', {
        'clients_count': clients_count,
        'projects_count': projects_count,
        'invoices_pending': invoices_pending,
        'invoices_paid': invoices_paid,
        'overdue_invoices': overdue_invoices,
    })