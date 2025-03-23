from django.db.models import Count
from django.db.models.functions import TruncMonth
from ..models import LostAndFound, Bookmark, Notification, Category, Attachment
from io import BytesIO
from django.db.models import Q, Count
from ..models import User, LostAndFound, Category  # 完整导入所有模型

# 在文件顶部添加
from django.db.models import Q, F, Func, Value, CharField, ExpressionWrapper

# 在文件顶部添加以下导入
from django.db.models import Q

# 修改generate_monthly_report函数中的Q对象引用
def generate_monthly_report():
    return list(  # 转换为可序列化列表
        LostAndFound.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(
            total=Count('id'),
            lost=Count('id', filter=Q(category__item_type='lost')),
            found=Count('id', filter=Q(category__item_type='found'))
        )
        .order_by('month')
        .annotate(month_str=ExpressionWrapper(
            Func(F('month'), Value('%Y-%m'), function='DATE_FORMAT'),  # 修改为MySQL日期格式化
            output_field=CharField()
        ))
        .values('month_str', 'total', 'lost', 'found')  # 使用格式化后的字段
    )

# 修改generate_category_report函数
def generate_category_report():
    return list(  # 转换为可序列化列表
        Category.objects
        .annotate(
            total=Count('lostandfound'),
            active=Count('lostandfound', filter=Q(lostandfound__status='active'))
        )
        .values('name', 'total', 'active')
    )

def generate_user_activity_report():
    return list(
        User.objects
        .annotate(
            post_count=Count('lostandfound'),
            login_count=Count('loginhistory_set', filter=Q(loginhistory_set__is_success=True))
        )
        .values(
            'username', 
            'post_count', 
            'login_count',
            last_login_time=Func(
                F('loginhistory_set__login_time'),
                Value('%Y-%m-%d %H:%i:%S'),
                function='DATE_FORMAT',
                output_field=CharField()  # 明确指定输出字段类型
            )
        )
    )

def export_to_excel(data):
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    
    if isinstance(data, list) and len(data) > 0:
        headers = list(data[0].keys())
        ws.append(headers)
        for row in data:
            ws.append([row.get(h) for h in headers])
    
    output = BytesIO()
    wb.save(output)
    return output.getvalue()
