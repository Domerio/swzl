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
