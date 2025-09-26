# invoices/models.py
from django.db import models
from projects.models import Project
from django.contrib.auth.models import User

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Overdue', 'Overdue'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Invoice {self.id} - {self.status}"