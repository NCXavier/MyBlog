from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
# 博客文章数据模型
class ArticlePost(models.Model):
    # 文章作者。参数 on_delete 用于指定删除的方式
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 文章标题，models.CharField 为字符串字段，用于保存较短的字符串，
    title = models.CharField(max_length=100)

    # 文章正文，保存大量文本使用TextField
    body = models.TextField()

    # 文章创建时间， 参数default=timezone.now
    created = models.DateTimeField(default=timezone.now)

    # 文章更新时间，参数auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)  # 根据created倒序排列

    def __str__(self):
        # return self.title 将文章标题返回
        return self.title
