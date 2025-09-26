from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freelancer_crm.settings')

# 🔥 Имя переменной должно быть "celery"
celery = Celery('freelancer_crm')

celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()