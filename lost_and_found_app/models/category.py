from django.db import models


class Category(models.Model):
    TYPE_CHOICES = (
        ('lost', '失物'),
        ('found', '招领')
    )

    name = models.CharField(max_length=20, verbose_name="分类名称")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name="父级分类")
    item_type = models.CharField(max_length=5, choices=TYPE_CHOICES, verbose_name="分类类型")
    icon = models.CharField(max_length=50, null=True, blank=True, verbose_name="图标样式")

    class Meta:
        verbose_name = "物品分类"
        verbose_name_plural = "物品分类"

    def __str__(self):
        return self.name
