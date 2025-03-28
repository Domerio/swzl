from django.db.models import Q
from datetime import timedelta
import logging
from django.utils import timezone
from ..models import LostAndFound, Notification, Category

logger = logging.getLogger(__name__)

def find_and_notify_matches(approved_item):
    # 记录匹配开始
    logger.info(f"🏁 开始智能匹配流程 - 物品ID: {approved_item.id} 类型: {approved_item.category.item_type}")
    
    try:
        # 匹配方向判断
        if approved_item.category.item_type == 'lost':
            match_type = 'found'  # 必须保留此变量初始化
            notification_template = "发现与您丢失的【{0}】相似的招领信息：{1}，{2}"
            logger.debug(f"🔍 匹配方向：失物 -> 招领 | 分类: {approved_item.category.name}")  # 需要恢复日志输出
        else:
            match_type = 'lost'
            notification_template = "发现与您招领的【{0}】相似的失物信息：{1}，{2}"
            logger.debug(f"🔍 匹配方向：招领 -> 失物 | 分类: {approved_item.category.name}")

        # 构建查询条件
        time_range = (
            approved_item.lost_time - timedelta(days=3),
            approved_item.lost_time + timedelta(days=3)
        )
        logger.debug(f"⏰ 时间范围: {time_range[0]} ~ {time_range[1]}")
        
        # 新增分类名称获取
        category_name = approved_item.category.name
        logger.debug(f"🗂️ 当前分类名称: {category_name} | 类型: {match_type}")
        
        # 修改后的查询条件（比较分类名称）
        query = Q(
            category__name=category_name,  # ← 这里改为比较name字段
            status='active',
            category__item_type=match_type,
            lost_time__range=time_range
        )
        
        # 地点敏感型物品处理（保持原逻辑）
        if category_name in ['证件', '钥匙']:  # ← 使用已获取的分类名称
            query &= Q(location=approved_item.location)
            logger.debug(f"📍 地点匹配启用 | 地点: {approved_item.location}")
            
        # 执行查询
        matches = LostAndFound.objects.filter(query).exclude(user=approved_item.user)
        logger.info(f"✅ 找到 {matches.count()} 个潜在匹配项")
        
        # 发送通知
        if matches:
            for match in matches:
                logger.debug(f"💌 发送通知：用户 {approved_item.user.id} <-[匹配]-> 用户 {match.user.id}")
                
                # 添加联系方式获取逻辑
                contact_info = match.user.phone or match.user.email  # 优先显示手机号
                match_contact_info = approved_item.user.phone or approved_item.user.email
                
                # 修改后的通知模板
                Notification.objects.create(
                    user=approved_item.user,
                    content=notification_template.format(
                        approved_item.title, 
                        match.title,
                        f"联系方式：{contact_info}" if contact_info else "（对方未提供联系方式）"
                    ),
                    notification_type="match",
                    related_item_id=match.id
                )
                
                Notification.objects.create(
                    user=match.user,
                    content=notification_template.format(
                        match.title,
                        approved_item.title,
                        f"联系方式：{match_contact_info}" if match_contact_info else "（对方未提供联系方式）"
                    ),
                    notification_type="match",
                    related_item_id=approved_item.id
                )
        return matches.count()
        
    except Exception as e:
        logger.error(f"❌ 匹配过程中发生异常: {str(e)}", exc_info=True)
        raise  # 保持原有异常处理流程
