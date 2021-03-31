from rest_framework import mixins, viewsets, filters
from article.serializers import ArticleSerializer, CategorySerializer, CategoryDetailSerializer, TagSerializer, \
    ArticleDetailSerializer, AvatarSerializer
from article.permissions import IsAdminUserOrReadOnly
from article.models import Article, Category, Tag, Avatar

"""文章视图集"""
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


"""分类视图集"""
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


"""标签视图集"""
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUserOrReadOnly]


"""图片视图集"""
class AvatarViewSet(viewsets.ModelViewSet):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = [IsAdminUserOrReadOnly]


"""之前的代码"""
# from django.http import Http404
# from article.serializers import ArticleListSerializer, ArticleDetailSerializer
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.decorators import api_view
# from rest_framework.permissions import IsAdminUser
# from rest_framework.response import Response
# from rest_framework.serializers import Serializer
# from rest_framework import generics
# from rest_framework.views import APIView
# from rest_framework import status
# from rest_framework import mixins

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