# lost_and_found_app/api/views/items.py
from flask import Response
from rest_framework import generics, status
from rest_framework import permissions  # 添加此行
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from ...models import LostAndFound, Category, Attachment
from ...serializers import LostItemSerializer, FoundItemSerializer


class LostAndFoundListCreateAPI(generics.ListCreateAPIView):
    # 指定使用的序列化器类，用于将模型实例转换为JSON格式
    serializer_class = LostItemSerializer
    # 指定权限类，确保只有经过身份验证的用户才能访问此API
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 获取当前视图的查询集，即过滤出状态为'active'的LostAndFound对象
        return LostAndFound.objects.filter(status='active')

    def perform_create(self, serializer):
        # 在创建新的LostAndFound对象时，自动将当前请求的用户关联到该对象
        serializer.save(user=self.request.user)


class LostItemCreateAPI(generics.CreateAPIView):
    queryset = LostAndFound.objects.all()
    serializer_class = LostItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def perform_create(self, serializer):
        # 自动关联当前用户
        lost_and_found = serializer.save(user=self.request.user)

        # 处理图片上传
        images = self.request.FILES.getlist('images')
        for image in images:
            Attachment.objects.create(
                image=image,
                item=lost_and_found
            )


class LostItemHallAPI(generics.ListAPIView):
    # 筛选状态为 'active' 且物品类型为 'lost' 的失物信息
    queryset = LostAndFound.objects.filter(status='active', category__item_type='lost')
    serializer_class = LostItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def get_queryset(self):
        return self.queryset.filter(status='active', category__item_type='lost')


class FoundItemHallAPI(generics.ListAPIView):
    queryset = LostAndFound.objects.filter(status='active')
    serializer_class = FoundItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def get_queryset(self):
        return self.queryset.filter(status='active')


class FoundItemCreateAPI(generics.CreateAPIView):
    queryset = LostAndFound.objects.all()
    serializer_class = FoundItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def perform_create(self, serializer):
        # 自动关联当前用户
        lost_and_found = serializer.save(user=self.request.user)
        # 处理图片上传
        images = self.request.FILES.getlist('images')
        for image in images:
            Attachment.objects.create(
                image=image,
                item=lost_and_found
            )


class SearchAPI(APIView):
    def get(self, request):
        from ...serializers import LostItemSerializer
        keyword = request.query_params.get('keyword')
        if keyword:
            results = LostAndFound.objects.filter(title__icontains=keyword)
        else:
            results = LostAndFound.objects.all()
        serializer = LostItemSerializer(results, many=True)
        return Response(serializer.data)


class UpdateStatusAPI(APIView):
    def post(self, request, pk):
        try:
            lost_and_found = LostAndFound.objects.get(pk=pk)
            status = request.data.get('status')
            result = request.data.get('result')
            lost_and_found.status = status
            lost_and_found.result = result
            lost_and_found.save()
            serializer = LostItemSerializer(lost_and_found)
            return Response({
                'status': 'success',
                'message': '状态更新成功',
                'data': serializer.data
            })
        except LostAndFound.DoesNotExist:
            return Response({
                'status': 'error',
                'message': '失物招领信息不存在'
            }, status=404)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'更新状态时发生错误: {str(e)}'
            }, status=500)


class LostCategoryListAPI(APIView):
    def get(self, request):
        from rest_framework.response import Response
        def build_tree(categories, parent_id=1):
            result = []
            for category in categories:
                if category.parent_id == parent_id:
                    children = build_tree(categories, category.id)
                    item = {
                        'id': category.id,
                        'name': category.name,
                        'children': children
                    }
                    result.append(item)
            return result

        all_categories = Category.objects.all()
        tree = build_tree(all_categories)
        return Response(tree)


class FoundCategoryListAPI(APIView):
    def get(self, request):
        from rest_framework.response import Response
        def build_tree(categories, parent_id=7):
            result = []
            for category in categories:
                if category.parent_id == parent_id:
                    children = build_tree(categories, category.id)
                    item = {
                        'id': category.id,
                        'name': category.name,
                        'children': children
                    }
                    result.append(item)
            return result

        all_categories = Category.objects.all()
        tree = build_tree(all_categories)
        return Response(tree)


class ItemDeleteView(APIView):
    def delete(self, request, pk):
        from rest_framework.response import Response
        try:
            item = LostAndFound.objects.get(pk=pk)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except LostAndFound.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
