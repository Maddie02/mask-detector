import pytz
from datetime import datetime

from ..models import Statistic

def delete_stats_if_a_month_have_passed(stat):
    
    company = stat.employee.company.name
    company_stats = Statistic.objects.filter(employee__company__name=company)

    for stat in company_stats:
        if stat == None:
            return
        
        today = pytz.utc.localize(datetime.now())

        if today.month != stat.last_seen_date.month:
            print(f"deleting statistic for {stat.employee}")
            stat.delete()
            stat = None

