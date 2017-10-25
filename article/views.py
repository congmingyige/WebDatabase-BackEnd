from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse
from django.core.urlresolvers import reverse
from article.models import Comment, Article
from user.models import User

# Create your views here.


def article_show(request):
    title = request.POST.get("title", None)
    author = request.POST.get("author", None)
    article = Article.objects.filter(title=title, author=author)
    if article is None:
        return HttpResponse("No this article")

    if request.method == 'POST':
        # 用户是否按下“喜欢该文章”的按钮
        liked = request.POST.get("liked", None)
        if not liked:
            article.liked = article.liked + 1
            article.save()
            return render(reverse("article" + str(article.id)), "article.html", {"article": article, "comment": article.comments_set.all()})
        # 该网页对文章、评论的处理函数
        return article_operation(request)

    # 用户是否曾经访问过此网页
    if not request.COOKIES["visit"]:
        article.views = article.views + 1
        article.save()
        response = render(reverse("article"+str(article.id)), "article.html", {"article": article, "comment": article.comments_set.all()})
        response.set_cookie("visit", "1")
        return response
    return render(reverse("article"+str(article.id)), "article.html", {"article": article, "comment": article.comments_set.all()})


def article_operation(request):

    title = request.POST.get("title", None)
    author = request.POST.get("author", None)
    article = Article.objects.filter(title=title, author=author)
    if article is None:
        return HttpResponse("No this article")

    # 修改、删除文章(评论)是需要作者和用户是相同的

    if request.method == "POST":
        if request.POST.get("article_create", None) is not None:
            article_create()
        elif request.POST.get("article_modify", None) is not None:
            article_modify()
        elif request.POST.get("article_delete", None) is not None:
            article_delete()
        elif request.POST.get("comment_create", None) is not None:
            comment_create()
        elif request.POST.get("comment_modify", None) is not None:
            comment_modify()
        elif request.POST.get("comment_delete", None) is not None:
            comment_delete()

    return render(reverse("article" + str(article.id)), "article.html", {"article": article, "comment": article.comments_set.all()})

# in article
def comment_create(request):

    # foreign key ：author 是啥 是一个对象 还是 一个主键(通过这个主键可以访问该对象)
    # 需要修改 ???
    # user = User.objects.filter(phone=username) + User.objects.filter(email=username)
    # ... comment = Comment(author=user, content=content)

    author = request.COOKIES["username"]
    content = request.POST.get("content", None)
    comment = Comment.objects.filter(author=author, content=content)
    if comment is not None:
        return HttpResponse("has already existed a comment the same author and content as this one")

    title = request.POST.get("title", None)
    author_article = request.POST.get("author", None)
    article = Article.objects.filter(title=title, author=author_article)
    if article is None:
        return HttpResponse("No this article")

    comment = Comment(author=author, content=content)
    comment.save()
    article.comments_set.add(comment)
    article.save()
    return HttpResponse("successfully create the comment")

# in article
def comment_modify(request):

    author = request.COOKIES["username"]
    content = request.POST.get("content", None)
    comment = Comment.objects.filter(author=author, content=content)
    if comment is None:
        return HttpResponse("No this comment")

    username = request.COOKIES["username"]
    if username != author:
        return HttpResponse("No authority")

    comment.content = content
    comment.save()
    return HttpResponse("successfully modify the comment")

# in article,user
def comment_delete(request):
    author = request.COOKIES["username"]
    content = request.POST.get("content", None)
    comment = Comment.objects.filter(author=author, content=content)
    if comment is None:
        return HttpResponse("No this comment")

    username = request.COOKIES["username"]
    if username != author:
        return HttpResponse("No authority")

    comment.delete()
    return HttpResponse("successfully delete a comment")

# in user
def article_create(request):

    title = request.POST.get("title", None)
    author = request.COOKIES["username"]
    article = Article.objects.filter(title=title, author=author)
    if article is not None:
        return HttpResponse("has already existed a article the same title and author as this one")

    text = request.POST.get("title", None)
    article = Article(title=title, author=author, text=text)
    article.save()
    return HttpResponse("successfully create the article")

# in article
def article_modify(request):

    title = request.POST.get("title", None)
    author = request.POST.get("author", None)
    article = Article.objects.filter(title=title, author=author)
    if article is None:
        return HttpResponse("No this article")

    username = request.COOKIES["username"]
    if username != author:
        return HttpResponse("No authority")

    text = request.POST.get("text", None)
    article.text = text
    article.save()
    return HttpResponse("successfully modify a article")

# in article,user
def article_delete(request):
    title = request.POST.get("title", None)
    author = request.POST.get("author", None)
    article = Article.objects.filter(title=title, author=author)
    if article is None:
        return HttpResponse("No this article")

    username = request.COOKIES["username"]
    if username != author:
        return HttpResponse("No authority")

    article.delete()
    return HttpResponse("successfully delete a article")


def user_content(request):
    username = request.COOKIES["username"]
    user = User.objects.filter(phone=username) + User.objects.filter(email=username)
    if request.method == 'POST':
        mode = request.POST.get("mode", None)
        if mode == "comment":
            comment = Comment.objects.filter(author=user)
            return render(request, "user_setting.html", {"comment": comment})

    article = Article.objects.filter(author=user)
    return render(request, "user_content.html", {"article": article})


 # <form action > 可以直接调用函数吗
 # 能直接返回原来的网页吗

'''
Django-数据库多对多关系
http://blog.csdn.net/y472360651/article/details/74315504

a.comments_set.add(XXX)  就可以增加文章a关联的评论

a.comments_set.all()  就能得到文章a关联的所有评论
这样就实现了我们期待的不经过查询筛选，直接获得文章对应的评论了
'''