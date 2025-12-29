from django.db import models
from django.contrib.auth.models import User

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    company_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)

    status = models.CharField(max_length=20)
    applied_date = models.DateField()
    deadline = models.DateField()
    notes = models.TextField(blank=True)

    role_type = models.IntegerField()     # 1 = tech, 0 = non-tech
    company_type = models.IntegerField()  # 1 = product, 0 = service

    prediction_score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.company_name} - {self.role}"
