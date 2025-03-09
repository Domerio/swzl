from django.db import models
from .user import User
from .item import LostAndFound


class Notification(models.Model):
    TYPE_CHOICES = (
        ('system', '系统通知'),
        ('match', '信息匹配'),
        ('reminder', '进度提醒')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="接收用户")
    content = models.TextField(verbose_name="通知内容")
    notification_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='system')
    is_read = models.BooleanField(default=False, verbose_name="已读状态")
    related_item = models.ForeignKey(LostAndFound, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="生成时间")

    class Meta:
        verbose_name = "消息通知"
        verbose_name_plural = "消息通知"
        ordering = ['-created_at']


def create_notification(user, content, related_item=None, notification_type='match'):
    Notification.objects.create(
        user=user,
        content=content,
        notification_type=notification_type,
        related_item=related_item
    )


def check_matches():
    lost_items = LostAndFound.objects.filter(status='active', item_type='lost')
    found_items = LostAndFound.objects.filter(status='active', item_type='found')

    for lost_item in lost_items:
        for found_item in found_items:
            if lost_item.category == found_item.category and lost_item.location == found_item.location:
                # 创建通知给失主
                create_notification(lost_item.user, f"你的失物 {lost_item.title} 可能已被找到，请查看招领信息。",
                                    found_item)
                # 创建通知给拾到者
                create_notification(found_item.user, f"你拾到的物品 {found_item.title} 可能有失主，请查看失物信息。",
                                    lost_item)
