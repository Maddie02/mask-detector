from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from .forms import SignUpEmployeeForm
from .models import Employee, Statistic
import datetime
import csv

def home(request):
    return render(request, 'accounts/home.html', {'home': 1})


def register(request):
    if request.method == 'POST':
        form = SignUpEmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            messages.success(request, f'{first_name}, your account has been created. You can now log in.')
            return redirect('login')
    else:
        form = SignUpEmployeeForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


@login_required
def export_csv_stats(request):

    utc = datetime.timedelta(hours=2)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Stats' + str(datetime.datetime.now() + utc) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['First name', 'Last name', 'Violations', 'Last date without mask'])

    stat = Statistic.objects.filter(employee=request.user).first()

    writer.writerow([stat.employee.first_name, stat.employee.last_name, stat.count_violations, stat.last_seen_date + utc])

    return response


@staff_member_required
def dashboard(request):
    employees = Employee.objects.all()
    stats = Statistic.objects.all()

    return render(request, 'accounts/dashboard.html', {'employees': employees, 'stats': stats})

