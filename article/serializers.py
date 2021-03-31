from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from article.models import Article, Category, Tag, Avatar
from user_info.serializers import UserDescSerializer




""" 分类 序列器 """
class CategorySerializer(serializers.HyperlinkedModelSerializer):
    # HyperlinkedIdentityField 将将路由间的表示转换为超链接 view_name 参数路由名
    url = serializers.HyperlinkedIdentityField(view_name='category-detail')

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created']


""" 图片 序列器 """
class AvatarSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='avatar-detail')

    class Meta:
        model = Avatar
        fields = '__all__'


""" 标签 序列器 """
class TagSerializer(serializers.HyperlinkedModelSerializer):

    # 重复创建两个 id 不同 但是 标签名称相同的 标签是没有意义的
    def check_tag_obj_exists(self, validated_data):
        t_tag = validated_data.get('t_tag')
        if Tag.objects.filter(t_tag=t_tag).exists():
            raise serializers.ValidationError(f'Tag with t_tag {t_tag} exists')

    # 重写创建 更新
    def create(self, validated_data):
        self.check_tag_obj_exists(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self.check_tag_obj_exists(validated_data)
        return super().update(instance, validated_data)

    class Meta:
        model = Tag
        fields = '__all__'



""" 文章 序列器 Base """
class ArticleBaseSerializer(serializers.HyperlinkedModelSerializer):
    # 用户模型设置为只读
    author = UserDescSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)
    tags = serializers.SlugRelatedField(queryset=Tag.objects.all(), many=True, required=False, slug_field='t_tag')
    avatar = AvatarSerializer()

    # to_internal_value() 允许改变我们反序列化的输出。
    # o_representation() 允许我们改变序列化的输出。

    def to_internal_value(self, data):
        tags_data = data.get('tags')
        for tag in tags_data:
            if not Tag.objects.filter(t_tag=tag).exists():
                Tag.objects.create(t_tag=tag)
        return super().to_internal_value(data)

    # 重写 序列化输出之前 to_representation 可以达到添加一个额外的参数
    # def to_representation(self, value):
    #     data = super().to_representation(value)
    #     data['tag_count'] = value.tags.count()
    #     return data

    # 全局验证器 validate() 接收参数为 所有字段的字典
    # 特定字段验证器 validate_{{ field_name }} () 指定字段的一个验证器
    # def validate_category_id(self, value):
    #     if not Category.objects.filter(id=value).exists() and value is not None:
    #         raise serializers.ValidationError(f"Category with id {value} not exists")
    #     return value
    #
    # def validate_avatar_id(self, value):
    #     if not Avatar.objects.filter(id=value).exists() and value is not None:
    #         raise serializers.ValidationError(f'Avatar with id {value} not exists')
    #     return value
    # 封装
    default_error_messages = {
        'incorrect_avatar_id': 'Avatar with id {value} not exists.',
        'incorrect_category_id': 'Category with id {value} not exists.',
        'default': 'No more message here..'
    }

    def check_obj_exists_or_fail(self, model, value, message='default'):
        if not self.default_error_messages.get(message):
            message = 'default'

        if not model.objects.filter(id=value).exists() and value is not None:
            self.fail(message, value=value)

    def validate_category_id(self, value):
        self.check_obj_exists_or_fail(model=Category, value=value, message='incorrect_category_id')

        return value

    def validate_avatar_id(self, value):
        self.check_obj_exists_or_fail(model=Article, value=value, message='incorrect_avatar_id')

        return value

    class Meta:
        model = Article
        fields = '__all__'


""" 分类详情的嵌套序列器 """
class ArticleCategoryDetailSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='article-detail')

    class Meta:
        model = Article
        fields = ['url', 'title']


""" 分类详情 序列器 """
class CategoryDetailSerializer(serializers.ModelSerializer):
    articles = ArticleCategoryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'created', 'articles']


""" 文章 序列器 """
class ArticleSerializer(ArticleBaseSerializer):
    class Meta:
        model = Article
        fields = "__all__"
        # 使用 extra_kwargs 设置不显示,但是可以写入
        extra_kwargs = {'body': {'write_only': True}}


""" 文章详情 序列器 """
class ArticleDetailSerializer(ArticleBaseSerializer):
    # 渲染后的正文
    body_html = serializers.SerializerMethodField()
    # 渲染后的目录
    toc_html = serializers.SerializerMethodField()

    def get_body_html(self, obj):
        return obj.get_md()[0]

    def get_toc_html(self, obj):
        return obj.get_md()[1]

    class Meta:
        model = Article
        fields = '__all__'


""" 之前写的代码 """
# class ArticleListSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(allow_blank=True, max_length=100)
#     body = serializers.CharField(allow_blank=True)
#     created = serializers.DateTimeField()
#     updated = serializers.DateTimeField()

#

# ModelSerializer
# class ArticleListSerializer(serializers.ModelSerializer):
#     url = serializers.HyperlinkedIdentityField(view_name="article:detail")
#     author = UserDescSerializer(read_only=True)
#     class Meta:
#         model = Article
#         # 所有字段
#         fields = ['title', 'body', 'author', 'url', 'created', 'updated']
#
#         # 设置只读字段 序列器就不处理此 字段了
#         # read_only_fields = ['author']
#
# class ArticleDetailSerializer(serializers.ModelSerializer):
#
#     # 添加超链接
#     # url = serializers.HyperlinkedIdentityField(view_name='article:detail')
#
#     class Meta:
#         model = Article
#         fields = '__all__'
