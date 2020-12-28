from django.urls import path
from . import views


app_name = 'article'

urlpatterns = [
    # path函数将url映射到视图
    path("article-list/", views.article_list, name="article_list")
]
