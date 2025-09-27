# invoices/models.py
from django.db import models
from projects.models import Project
from django.contrib.auth.models import User

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Ожидает'),
        ('Paid', 'Оплачен'),
        ('Overdue', 'Просрочен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="Проект")
    amount = models.DecimalField("Сумма", max_digits=10, decimal_places=2)
    due_date = models.DateField("Дата оплаты")
    status = models.CharField("Статус", max_length=10, choices=STATUS_CHOICES, default='Pending')
    notes = models.TextField("Примечания", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Счёт #{self.id} — {self.project.name}"

    class Meta:
        verbose_name = "Счёт"
        verbose_name_plural = "Счета"