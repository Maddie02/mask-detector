from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import pre_save
from django.dispatch import receiver
from camera.controller import CameraThread
from .models import Company
from .models import Employee


@receiver(pre_save, sender=Employee)
def add_employee_to_company(sender, instance, **kwargs):
    employee_email_domain = instance.email.partition("@")[2]
    company = Company.objects.filter(email_domain=employee_email_domain)

    if company:
        instance.company = company.first()


@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    camera_thread = CameraThread(user)
    camera_thread.daemon = True
    camera_thread.start()

