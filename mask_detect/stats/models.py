from django.db import models
from accounts.models import Employee

class Statistic(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, null=True)
    count_violations = models.IntegerField(null=True)
    last_seen_date = models.DateTimeField(null=True)
    
    def __str__(self):
        return f'{self.employee.first_name} {self.employee.last_name}'

