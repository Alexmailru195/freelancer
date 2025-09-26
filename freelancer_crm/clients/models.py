from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField("Имя", max_length=100)
    email = models.EmailField("Email", unique=True)
    phone = models.CharField("Телефон", max_length=20, blank=True)
    company = models.CharField("Компания", max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"