from django.contrib.auth.models import User
from django.db import models
from markdown import Markdown


class Tag(models.Model):
    """文章标签"""
    t_tag = models.CharField(max_length=30)

    class Meta:
        db_table = 'Tag'
        ordering = ['-id']

    def __str__(self):
        return f"<Tag:{self.t_tag}>"


class Category(models.Model):
    """文章分类"""
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"<Category:{self.title}>"

    class Meta:
        db_table = 'Category'


class Article(models.Model):
    """文章"""
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles')
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='articles')
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<Article:{self.title}>"

    def get_md(self):
        md = Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        md_body = md.convert(self.body)
        return md_body, md.toc

    class Meta:
        db_table = 'Article'
        ordering = ['-created']


