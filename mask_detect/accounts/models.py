from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.utils import timezone

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

    def remove_on_image_update(self):
        try:
            employee = Employee.objects.get(id=self.id)
        except:
            return
        
        if employee.profile_pic and self.profile_pic and employee.profile_pic != self.profile_pic:
            employee.profile_pic.delete()
        
    def delete(self, *args, **kwargs):
        self.profile_pic.delete()
        return super(Employee, self).delete(*args, *kwargs)
    
    def save(self, *args, **kwargs):
        self.remove_on_image_update()
        return super(Employee, self).save(*args, **kwargs)


    
