from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Company
from .models import Employee
from stats.models import Statistic
from stats.utils.check_stats import delete_stats_if_a_month_have_passed


@receiver(pre_save, sender=Employee)
def add_employee_to_company(sender, instance, **kwargs):
    employee_email_domain = instance.email.partition("@")[2]
    company = Company.objects.filter(email_domain=employee_email_domain)

    if company:
        instance.company = company.first()



