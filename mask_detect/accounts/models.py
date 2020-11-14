from django.db import models
from django.contrib.auth.models import AbstractUser

class Company(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Employee(AbstractUser):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profilepics/', blank=True, null=True)

