from django.db import models
from .user import User


class Report(models.Model):
    REPORT_TYPE_CHOICES = (
        ('daily', '日报'),
        ('weekly', '周报'),
        ('monthly', '月报'),
        ('custom', '自定义分析')
    )

    title = models.CharField(max_length=50, verbose_name="报表标题")
    report_type = models.CharField(max_length=10, choices=REPORT_TYPE_CHOICES)
    start_date = models.DateField(verbose_name="开始日期")
    end_date = models.DateField(verbose_name="结束日期")
    content = models.JSONField(verbose_name="统计内容")
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="生成人")
    generated_at = models.DateTimeField(auto_now_add=True, verbose_name="生成时间")

    class Meta:
        verbose_name = "统计报表"
        verbose_name_plural = "统计报表"
