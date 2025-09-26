import json

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Project
from .forms import ProjectForm
from clients.models import Client

@login_required
def project_list(request):
    query = request.GET.get('q')
    projects = Project.objects.filter(user=request.user)
    if query:
        projects = projects.filter(
            Q(name__icontains=query) |
            Q(client__name__icontains=query)
        )
    clients = Client.objects.filter(user=request.user).order_by('name')
    return render(request, 'projects/project_list.html', {
        'projects': projects,
        'clients': clients
    })

@csrf_exempt
@login_required
def project_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            data['client'] = int(data['client'])
            form = ProjectForm(data)
            if form.is_valid():
                project = form.save(commit=False)
                project.user = request.user
                project.save()

                # ✉️ Отправляем письмо клиенту
                client = project.client
                send_mail(
                    subject=f"Проект '{project.name}' создан",
                    message=f"""
Здравствуйте, {client.name}!

Мы начали работу над проектом "{project.name}".
Дата начала: {project.start_date}
Дата окончания: {project.end_date or 'не указана'}

Спасибо за доверие!
                    """,
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

@csrf_exempt
@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            data['client'] = int(data['client'])
            form = ProjectForm(data, instance=project)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    if request.method == 'POST':
        project.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Method not allowed'}, status=405)