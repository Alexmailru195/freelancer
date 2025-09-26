# projects/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Project
from datetime import date

@shared_task
def send_daily_project_updates():
    today = date.today()
    sent_count = 0

    # Проекты, которые начинаются сегодня
    starting_projects = Project.objects.filter(start_date=today)
    for project in starting_projects:
        send_mail(
            subject=f"🚀 Начало проекта '{project.name}'",
            message=f"""
Здравствуйте, {project.client.name}!

Рады сообщить, что сегодня начинается проект **{project.name}**.
Мы уже приступили к работе и будем держать вас в курсе.

Дата начала: {project.start_date}
Дата окончания: {project.end_date or 'Не указана'}

С уважением,
Команда {settings.SITE_NAME or 'Freelancer CRM'}
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[project.client.email],
            fail_silently=False,
        )
        sent_count += 1

    # Проекты, которые заканчиваются сегодня
    ending_projects = Project.objects.filter(end_date=today)
    for project in ending_projects:
        send_mail(
            subject=f"✅ Завершение проекта '{project.name}'",
            message=f"""
Здравствуйте, {project.client.name}!

Хорошие новости — проект **{project.name}** успешно завершён!
Благодарим за сотрудничество.

Если потребуется поддержка или доработки — мы всегда на связи.

С уважением,
Команда {settings.SITE_NAME or 'Freelancer CRM'}
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[project.client.email],
            fail_silently=False,
        )
        sent_count += 1

    return f"Отправлено {sent_count} писем."