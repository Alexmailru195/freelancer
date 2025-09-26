from django.db import models
from clients.models import Client
from django.contrib.auth.models import User

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клиент")
    name = models.CharField("Название", max_length=100)
    description = models.TextField("Описание", blank=True)
    start_date = models.DateField("Дата начала")
    end_date = models.DateField("Дата окончания", blank=True, null=True)
    budget = models.DecimalField("Бюджет", max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.client.name})"

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"