from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Statistic, Violation
from accounts.models import Employee, Company
from django.http import HttpResponse
from .utils.check_stats import delete_stats_if_a_month_have_passed
import plotly.graph_objects as go
import plotly.offline as opy
import datetime, pytz
import csv


def get_employee_stats(stats, company):

    stats_dict = {}

    for stat in stats:
        stats_dict[stat.employee.first_name + ' ' + stat.employee.last_name] = stat.all_violations
    
    employees = list(stats_dict.keys())
    violations = list(stats_dict.values())

    data = [go.Bar(
            x=employees, y=violations,
            marker=dict(
                line=dict(
                    color='rgb(8,48,107)',
                    width=1
                ),
            ),
            textposition='auto',
            opacity=0.8,
            )]

    layout = go.Layout(
        title="Violations of all employees" if company == None else f"Violations in {company}",
        font=dict(
            family='Poppins, monospace',
            size=14,
            color='#7f7f7f'))

    figure = go.Figure(data=data, layout=layout)
    figure.update_xaxes(
        title='Employee'
    )

    figure.update_yaxes(
        title='Violations'
    )

    chart = opy.plot(figure, output_type='div')

    return chart


def get_detailed_chart_for_employee(violations):

    detailed_violations = {}

    for violation in violations:
        key = violation.violation_date.strftime("%d. %B %Y")
        if key in detailed_violations:
            detailed_violations[key] += 1
        else:
            detailed_violations[key] = 1

    violation_dates = list(detailed_violations.keys())
    all_violations_per_date = list(detailed_violations.values())

    if len(violation_dates) < 3:
        return

    data = [go.Scatter(
            x=violation_dates, y=all_violations_per_date,
            textposition='bottom center',
            )]

    layout = go.Layout(
        title=f"Violation chart - {violations[0].statistic.employee}",
        font=dict(
            family='Poppins, monospace',
            size=14,
            color='#7f7f7f'))

    figure = go.Figure(data=data, layout=layout)
    figure.update_xaxes(
        title='Date'
    )

    figure.update_yaxes(
        title='Violations'
    )

    figure.update_layout(title_x=0.5)

    chart = opy.plot(figure, output_type='div')

    return chart


@staff_member_required
def export_csv_stats(request):
    
    employee_id = request.GET['employee_id']
    tz = pytz.timezone('Europe/Sofia')

    employee = Employee.objects.filter(id=employee_id).first()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Stats-' + employee.first_name + ' ' + employee.last_name + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Violation dates'])

    stat = Statistic.objects.filter(employee__id=employee_id).first()
    violations = Violation.objects.filter(statistic=stat)

    if stat == None:
        messages.info(request, 'Statistics for this account are not found')
        return redirect('profile')

    for v in violations:
        writer.writerow([v.violation_date.astimezone(tz)])
    
    return response


@staff_member_required
def dashboard(request):
    employees = Employee.objects.all() if request.user.is_superuser else Employee.objects.filter(company=request.user.company)
 
    company_stats = Statistic.objects.filter(employee__company__name=request.user.company)
    updated_stats = Statistic.objects.all() if request.user.is_superuser else company_stats

    disable = 'disabled' if len(company_stats) == 0 else None

    context = {
        'employees': employees,
        'stats': updated_stats,
        'disable': disable,
    }

    return render(request, 'accounts/dashboard.html', context)


@staff_member_required
def dashboard_export_csvs(request):
    tz = pytz.timezone('Europe/Sofia')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Stats' + str(datetime.datetime.now(tz)) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['First name', 'Last name', 'Violations', 'Last date without mask'])
    
    if request.user.is_superuser:
        stats = Statistic.objects.all()
    else:
        stats = Statistic.objects.filter(employee__company__name=request.user.company)

    if not stats:
        messages.info(request, 'There are no statistics available')
        return redirect('dashboard')

    for stat in stats:
        writer.writerow([stat.employee.first_name, stat.employee.last_name, stat.all_violations, stat.last_seen_without_mask.astimezone(tz=tz)])

    return response


@staff_member_required
def delete_dashboard_stats(request):
    Statistic.objects.filter(employee__company__name=request.user.company).delete()

    return redirect('dashboard')


@staff_member_required
def view_charts(request):

    companies = Company.objects.all()
    stats = Statistic.objects.all()

    charts_for_company = []

    for company in companies:
        stats_per_company = Statistic.objects.filter(employee__company__name=company)
        charts_for_company.append(get_employee_stats(stats_per_company, company=company))

    if request.user.is_superuser:
        context = {
            'chart': get_employee_stats(stats, company=None),
            'charts_for_company': charts_for_company,
        }
    else:
        stats_for_company = Statistic.objects.filter(employee__company__name=request.user.company)
        context = {
            'chart': get_employee_stats(stats_for_company, company=request.user.company)
        }
    
    return render(request, 'accounts/charts.html', context)

