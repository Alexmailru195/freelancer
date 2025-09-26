import csv
import json
import logging
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError

from .models import Client
from .forms import ClientForm

# Настройка логирования
logger = logging.getLogger(__name__)

@login_required
def client_list(request):
    query = request.GET.get('q')
    clients = Client.objects.filter(user=request.user)
    if query:
        clients = clients.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(company__icontains=query)
        )
    return render(request, 'clients/client_list.html', {'clients': clients})

@csrf_exempt
@login_required
def client_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.info(f"Получены данные: {data}")

            form = ClientForm(data)
            if form.is_valid():
                client = form.save(commit=False)
                client.user = request.user
                client.save()
                logger.info(f"Клиент сохранён: {client.id} - {client.name}")
                return JsonResponse({
                    'success': True,
                    'client': {
                        'id': client.id,
                        'name': client.name,
                        'email': client.email,
                        'phone': client.phone,
                        'company': client.company
                    }
                })
            else:
                logger.error(f"Ошибки формы: {form.errors}")
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        except Exception as e:
            logger.error(f"Ошибка в client_create: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
@login_required
def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk, user=request.user)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = ClientForm(data, instance=client)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    # Для GET — можно вернуть данные (не используется, т.к. форма заполняется через JS)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
def export_clients_csv(request):
    # Получаем клиентов текущего пользователя
    clients = Client.objects.filter(user=request.user)

    # Создаём HTTP-ответ с типом CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="clients.csv"'

    # Создаём writer и записываем заголовки
    writer = csv.writer(response)
    writer.writerow(['Имя', 'Email', 'Телефон', 'Компания'])

    # Записываем данные клиентов
    for client in clients:
        writer.writerow([client.name, client.email, client.phone, client.company])

    return response

@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk, user=request.user)
    if request.method == 'POST':
        client.delete()
        return redirect('clients:client_list')
    return render(request, 'clients/client_confirm_delete.html', {'client': client})