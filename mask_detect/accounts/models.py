from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import pre_save

class Company(models.Model):
    name = models.CharField(max_length=50)
    email_domain = models.CharField(max_length=50, unique=True, null=True)

    def __str__(self):
        return self.name


class Employee(AbstractUser):
    email = models.EmailField(unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    profile_pic = models.ImageField(upload_to='profilepics/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


@receiver(pre_save, sender=Employee)
def add_employee_to_company(sender, instance, **kwargs):
    employee_email_domain = instance.email.partition("@")[2]
    company = Company.objects.filter(email_domain=employee_email_domain)

    if company:
        instance.company = company.first()

