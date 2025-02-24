from django.db import models
from .user import User
from .category import Category


class LostAndFound(models.Model):
    STATUS_CHOICES = (
        ('pending', '待审核'),
        ('active', '进行中'),
        ('completed', '已完成'),
        ('expired', '已过期')
    )
    RESULT_CHOICES = (
        ('unclaimed', '未认领'),
        ('returned', '已归还'),
        ('invalid', '信息无效')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="关联用户")
    is_anonymous = models.BooleanField(default=False, verbose_name="匿名发布")
    title = models.CharField(max_length=50, verbose_name="标题")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="物品分类")
    description = models.TextField(verbose_name="详细描述")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="状态")
    result = models.CharField(max_length=10, choices=RESULT_CHOICES, null=True, blank=True, verbose_name="处理结果")
    lost_time = models.DateTimeField(verbose_name="丢失/拾取时间")
    location = models.CharField(max_length=100, verbose_name="地点")
    location_lat = models.FloatField(null=True, blank=True, verbose_name="纬度")
    location_lng = models.FloatField(null=True, blank=True, verbose_name="经度")
    contact = models.CharField(max_length=50, verbose_name="联系方式")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "失物招领信息"
        verbose_name_plural = "失物招领信息"
        indexes = [models.Index(fields=['status', 'created_at'])]

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
