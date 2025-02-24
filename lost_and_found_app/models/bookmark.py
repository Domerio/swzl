from django.db import models
from .user import User
from .item import LostAndFound


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    item = models.ForeignKey(LostAndFound, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'item')
        verbose_name = "用户收藏"
        verbose_name_plural = "用户收藏"
