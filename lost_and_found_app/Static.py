from django.db.models import Count
from .models import LostAndFound, Category


def get_frequent_lost_items():
    # 添加层级过滤，只获取叶子节点分类
    frequent_items = (
        LostAndFound.objects.filter(
            category__item_type="lost", category__parent__isnull=False  # 排除父级分类
        )
        .values("category__name")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    return frequent_items


def get_common_lost_locations():
    common_locations = (
        LostAndFound.objects.filter(category__item_type="lost")
        .values("location")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    return common_locations


def get_monthly_lost_rate():
    # 计算月度丢失率逻辑
    pass


def get_claim_success_rate():
    # 计算认领成功率逻辑
    pass
