from django.db import models
from django.contrib.auth.models import User

class Application(models.Model):

    STATUS_CHOICES = [
        ('APPLIED', 'Applied'),
        ('OA', 'Online Assessment'),
        ('INTERVIEW', 'Interview'),
        ('OFFER', 'Offer'),
        ('REJECTED', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPLIED')
    applied_date = models.DateField()
    deadline = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.company_name} - {self.role}"
