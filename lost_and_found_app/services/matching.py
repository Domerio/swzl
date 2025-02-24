# lost_and_found_app/services/matching.py
from django.db.models import Q

from lost_and_found_app.models import LostAndFound


def find_matching_items(new_item):
    return LostAndFound.objects.filter(
        Q(title__icontains=new_item.title) &
        Q(category=new_item.category)
    )
