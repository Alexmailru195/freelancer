# projects/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Project
from datetime import date

@shared_task
def send_daily_project_updates():
    today = date.today()
    sent = 0

    # Проекты, которые начинаются сегодня
    for project in Project.objects.filter(start_date=today):
        send_mail(
            subject=f"🚀 Начало проекта: {project.name}",
            message=f"Здравствуйте, {project.client.name}!\n\nВаш проект '{project.name}' начинается сегодня.\n\nС уважением, команда Freelancer CRM",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[project.client.email],
            fail_silently=False,
        )
        sent += 1

    # Проекты, которые заканчиваются сегодня
    for project in Project.objects.filter(end_date=today):
        send_mail(
            subject=f"✅ Завершение проекта: {project.name}",
            message=f"Здравствуйте, {project.client.name}!\n\nПроект '{project.name}' успешно завершён.\n\nСпасибо за сотрудничество!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[project.client.email],
            fail_silently=False,
        )
        sent += 1

    return f"Отправлено {sent} писем."