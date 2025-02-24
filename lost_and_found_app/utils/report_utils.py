from django.db.models import Count
from ..models import LostAndFound
from datetime import datetime, timedelta


def generate_monthly_report():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    data = LostAndFound.objects.filter(
        created_at__range=(start_date, end_date)
    ).values('category__name').annotate(total=Count('id'))
    return {
        'period': f"{start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}",
        'categories': list(data)
    }
