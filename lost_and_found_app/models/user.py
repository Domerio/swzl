from django.db import models
from django.contrib.auth.models import AbstractUser


# 在User模型中补充登录历史关联
class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', '学生'),
        ('staff', '教职工'),
        ('admin', '管理员'),
    )

    username = models.CharField(max_length=20, unique=True, verbose_name="学号/工号")
    real_name = models.CharField(max_length=20, verbose_name="真实姓名")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student', verbose_name="角色")
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name="联系电话")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="头像")
    is_verified = models.BooleanField(default=False, verbose_name="认证状态")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"
        permissions = [
            ("manage_content", "可以管理所有内容"),
            ("view_statistics", "可以查看统计报表"),
        ]

    def __str__(self):
        return f"{self.real_name}({self.role})"

    
    @property
    def login_records(self):
        return self.loginhistory_set.all()

class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loginhistory_set')
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    is_success = models.BooleanField(default=True)
