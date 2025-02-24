from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LostAndFound, Notification
from .services.matching import find_matching_items


@receiver(post_save, sender=LostAndFound)
def create_match_notification(sender, instance, created, **kwargs):
    if created:
        # 匹配逻辑：同一分类下标题相似的信息
        matches = find_matching_items(instance)  # 调用服务层
