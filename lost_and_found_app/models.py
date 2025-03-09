from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', '学生'),
        ('staff', '教职工'),
        ('admin', '管理员'),
    )
    
    name = models.CharField('姓名', max_length=50)
    role = models.CharField('角色', max_length=10, choices=ROLE_CHOICES, default='student')
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return f'{self.name}({self.get_role_display()})'