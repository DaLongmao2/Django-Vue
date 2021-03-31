# from django.http import Http404
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.decorators import api_view
# from rest_framework.permissions import IsAdminUser
# from rest_framework.response import Response
# from rest_framework.serializers import Serializer
# from rest_framework.views import APIView
from rest_framework import mixins, viewsets, filters
# from rest_framework import generics
from article.serializers import ArticleSerializer, CategorySerializer, CategoryDetailSerializer, TagSerializer, \
    ArticleDetailSerializer
from article.permissions import IsAdminUserOrReadOnly
# from article.serializers import ArticleListSerializer, ArticleDetailSerializer
from article.models import Article, Category, Tag


# from rest_framework import status

# 文章列表
# @api_view(['GET', 'POST'])
# def article_list(request):
#     if request.method == 'GET':
#         articles = Article.objects.all()
#         serializer = ArticleListSerializer(articles, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ArticleListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


# class ArticleDetail(APIView):
#     """文章详细视图"""
#
#     def get_object(self, pk):
#         try:
#             return Article.objects.get(pk=pk)
#         except:
#             raise Http404
#
#     def get(self, request, pk):
#         article = self.get_object(pk)
#         serializer = ArticleListSerializer(article)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         article = self.get_object(pk)
#         serializer = ArticleListSerializer(article, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         article = self.get_object(pk)
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class ArticleDetail(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleListSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

# ===========

# class ArticleList(generics.ListCreateAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleListSerializer
#     permission_classes = [IsAdminUserOrReadOnly]
#     # 新增的这个 perform_create() 从父类 ListCreateAPIView 继承而来，它在序列化数据真正保存之前调用，因此可以在这里添加额外的数据（即用户对象）。
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)
#
# class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleDetailSerializer


class ArticleViewSet(viewsets.ModelViewSet):

    queryset = Article.objects.all()

    # 文章序列化
    # serializer_class = ArticleSerializer
    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleSerializer
        else:
            return ArticleDetailSerializer
    # 权限
    permission_classes = [IsAdminUserOrReadOnly]

    # 筛选
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset =  Category.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]
    # serializer_class = CategorySerializer
    # 重写 serializer_class
    def get_serializer_class(self):
        print(self.action)
        if self.action == 'list':
            return CategorySerializer
        else:
            return CategoryDetailSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUserOrReadOnly]