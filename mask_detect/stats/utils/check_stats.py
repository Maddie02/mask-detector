import pytz
from datetime import datetime

from ..models import Statistic

def delete_stats_if_a_month_have_passed(stat):
    
    company = stat.employee.company.name
    company_stats = Statistic.objects.filter(employee__company__name=company)

    last_stat_for_company = company_stats.order_by('last_seen_date').last()

    if last_stat_for_company == None:
        return

    today = pytz.utc.localize(datetime.now())

    if today.month != last_stat_for_company.last_seen_date.month:
        print(f"deleting statistic for {company}")
        company_stats.delete()
        company_stats = None

