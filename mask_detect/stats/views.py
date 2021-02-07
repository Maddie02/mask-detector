from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Statistic
from accounts.models import Employee
from django.http import HttpResponse
import datetime
import csv


@login_required
def export_csv_stats(request):

    utc = datetime.timedelta(hours=2)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Stats' + str(datetime.datetime.now() + utc) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['First name', 'Last name', 'Violations', 'Last date without mask'])

    stat = Statistic.objects.filter(employee=request.user).first()

    if stat == None:
        messages.info(request, 'Statistics for your account are not found')
        return redirect('profile')

    writer.writerow([stat.employee.first_name, stat.employee.last_name, stat.count_violations, stat.last_seen_date + utc])

    return response


@staff_member_required
def dashboard(request):
    employees = Employee.objects.all()
    stats = Statistic.objects.all()

    return render(request, 'accounts/dashboard.html', {'employees': employees, 'stats': stats})


@staff_member_required
def dashboard_export_csvs(request):
    utc = datetime.timedelta(hours=2)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Stats' + str(datetime.datetime.now() + utc) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['First name', 'Last name', 'Violations', 'Last date without mask'])

    stats = Statistic.objects.all()

    for stat in stats:
        writer.writerow([stat.employee.first_name, stat.employee.last_name, stat.count_violations, stat.last_seen_date + utc])

    return response


@staff_member_required
def delete_dashboard_stats(request):
    Statistic.objects.all().delete()

    return redirect('dashboard')

