# invoices/views.py
import json

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Invoice
from .forms import InvoiceForm
from projects.models import Project

@login_required
def invoice_list(request):
    query = request.GET.get('q')
    invoices = Invoice.objects.filter(user=request.user)
    if query:
        invoices = invoices.filter(
            Q(project__name__icontains=query) |
            Q(project__client__name__icontains=query)
        )
    projects = Project.objects.filter(user=request.user)
    return render(request, 'invoices/invoice_list.html', {
        'invoices': invoices,
        'projects': projects
    })

@csrf_exempt
@login_required
def invoice_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            data['project'] = int(data['project'])
            form = InvoiceForm(data)
            if form.is_valid():
                invoice = form.save(commit=False)
                invoice.user = request.user
                invoice.save()

                # ✉️ Отправка письма клиенту
                client = invoice.project.client
                from django.core.mail import send_mail
                from django.conf import settings
                send_mail(
                    subject=f"Счёт #{invoice.id} по проекту '{invoice.project.name}'",
                    message=f"Здравствуйте, {client.name}!\n\nВыставлен счёт на сумму {invoice.amount}.\nДата оплаты: {invoice.due_date}\n\nС уважением, Freelancer CRM",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[client.email],
                    fail_silently=False,
                )

                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# invoices/views.py
from django.http import HttpResponse
from .utils import generate_invoice_pdf

@login_required
def invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, user=request.user)
    pdf_buffer = generate_invoice_pdf(invoice)
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.id}.pdf"'
    return response

@csrf_exempt
@login_required
def invoice_send(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, user=request.user)
    if request.method == 'POST':
        try:
            client = invoice.project.client
            send_mail(
                subject=f"Счёт #{invoice.id} по проекту '{invoice.project.name}'",
                message=f"Здравствуйте, {client.name}!\n\nВыставлен счёт на сумму {invoice.amount}.\nДата оплаты: {invoice.due_date}\n\nС уважением, Freelancer CRM",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[client.email],
                fail_silently=False,
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)