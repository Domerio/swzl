# lost_and_found_app/api/views/items.py
from flask import Response
from rest_framework import generics
from rest_framework import permissions  # 添加此行
from rest_framework.views import APIView

from ...models import LostAndFound, Category
from ...serializers import LostAndFoundSerializer


class LostAndFoundListCreateAPI(generics.ListCreateAPIView):
    serializer_class = LostAndFoundSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LostAndFound.objects.filter(status='active')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LostItemCreateAPI(generics.CreateAPIView):
    queryset = LostAndFound.objects.all()
    serializer_class = LostAndFoundSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # 自动关联当前用户
        serializer.save(user=self.request.user)


class CategoryListAPI(APIView):
    def get(self, request):
        from ...serializers import CategorySerializer
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class SearchAPI(APIView):
    def get(self, request):
        from ...serializers import LostAndFoundSerializer
        keyword = request.query_params.get('keyword')
        if keyword:
            results = LostAndFound.objects.filter(title__icontains=keyword)
        else:
            results = LostAndFound.objects.all()
        serializer = LostAndFoundSerializer(results, many=True)
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
            serializer = LostAndFoundSerializer(lost_and_found)
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
