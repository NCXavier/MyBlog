from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
import markdown
from .forms import ArticlePostForm
from .models import ArticlePost

# Create your views here.

def article_list(request):
    # 取出所有博客文章
    articles = ArticlePost.objects.all()
    # 需要传递给模板的对象
    context = {"articles": articles}
    return render(request, 'article/list.html', context)


def article_detail(request, id):
    # 取出相应的文章
    article = ArticlePost.objects.get(id=id)
    article.body = markdown.markdown(article.body,
        extensions=[
        # 包含 缩写、表格等常用扩展
        "markdown.extensions.extra",
        # 语法高亮扩展
        "markdown.extensions.codehilite",
        ]
    )
    # 需要传递给模板的对象
    context = {"article": article}
    # 载入模板，并返回context对象
    return render(request, "article/detail.html", context)

# 写文章的视图
def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定数据库id=1的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户id
            new_article.author = User.objects.get(id=1)
            # 将新文章保存到数据库中
            new_article.save()
            # 完成后返回到文章列表
            return redirect("article:article_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        context = {"article_post_form": article_post_form}
        # 返回模板
        return render(request, "article/create.html", context)

# 删文章
def article_delete(request, id):
    # 根据id获取需要删除的文章
    article = ArticlePost.objects.get(id=id)
    # 调用.delete()方法删除文章
    article.delete()
    # 完成删除后返回文章列表
    return redirect("article:article_list")


# 安全删除文章
def article_safe_delete(request, id):
    if request.method == "POST":
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")


# 更新文章
def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新title、body字段
    GET方法进入初始单页面
    id: 文章id
    """
    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)
    # 判断用户是否为POST提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例里面
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的title\body数据并保存
            article.title = request.POST["title"]
            article.body = request.POST["body"]
            article.save()
            # 完成后返回到修改后的文章中，需要传入文章的id值
            return redirect("article:article_detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户Get请求获取数据
    else:
        # 创建表单实例
        article_post_form = ArticlePostForm()
        # 赋值上下文，将article文章对象也传递进去，以便提取旧的内容
        context = {"article": article, "article_post_form": article_post_form}
        # 将响应返回模板中
        return render(request, "article/update.html", context)
