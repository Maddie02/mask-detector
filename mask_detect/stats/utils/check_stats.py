import pytz
from datetime import datetime

from ..models import Statistic

def delete_stats_if_a_month_have_passed(stat):
    
    company = stat.employee.company.name
    company_stats = Statistic.objects.filter(employee__company__name=company)

    first_stat_for_company = company_stats.order_by('last_seen_date').first()

    if first_stat_for_company == None:
        return

    delta = pytz.utc.localize(datetime.now()) - first_stat_for_company.last_seen_date

    if delta.days >= 30:
        print(f"deleting statistic for {company}")
        company_stats.delete()
        company_stats = None

