from django.db import models
from accounts.models import Employee

class Statistic(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, null=True)
    all_violations = models.IntegerField(default=0)
    last_seen_without_mask = models.DateTimeField(null=True)

    def __str__(self):
        return f'Statistic - {self.employee.first_name} {self.employee.last_name}'


class Violation(models.Model):
    violation_date = models.DateTimeField()
    frame = models.ImageField(upload_to='violations/', blank=True, null=True)
    statistic = models.ForeignKey(Statistic, on_delete=models.CASCADE)

    def __str__(self):
        return f'Violation - {self.statistic.employee.first_name} {self.statistic.employee.last_name}'

