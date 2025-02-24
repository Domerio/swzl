from django.db import models
from .item import LostAndFound


class Attachment(models.Model):
    item = models.ForeignKey(LostAndFound, on_delete=models.CASCADE, related_name='attachments')
    image = models.ImageField(upload_to='lost_found/%Y/%m/', verbose_name="物品图片")
    is_primary = models.BooleanField(default=False, verbose_name="主图")

    class Meta:
        verbose_name = "附件管理"
        verbose_name_plural = "附件管理"
