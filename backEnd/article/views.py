from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse
from article.models import Comment, Article

# Create your views here.


def article_show(request):
    title = request.POST.get("title", None)
    author = request.POST.get("author", None)
    if Article.objects.filter(title=title,author=author):
        
    return HttpResponse("No this article")

def article_modify(request):
    # 是否进行操作
    operation = False

    def comment_create():
        content = request.POST.get("content", None)
        author = request.POST.get("username", None)
        if content is not None and author is not None:
            comment = Comment(content=content, author=author)
            comment.save()
            article.comments_set.add(comment)
            article.save()

    def comment_modify():
        content = request.POST.get("content", None)
        comment = Comment.objects.filter(author=request.session["username"])
        if comment is not None:
            comment.content = content
            comment.save()
            return HttpResponse("Successfully modify the comment")
        else:
            return HttpResponse("No this comment")
    def comment_delete():
        comment = Comment.objects.filter(author=request.session["username"], content=request.POST.get("content", None))
        if comment is not None:
            comment.delete()

    article = Article.objects.filter(title=request.POST.get("title", None), author=request.POST.get("author", None))
    if not article:
        return HttpResponse("No this article")

    if request.method == "POST":
        if request.POST.get("likes", None) is not None:
            if article.likes != 32767:
                article.likes = article.likes + 1
                article.save()
            operation = True
        elif request.POST.get("comment_submit", None) is not None:
            comment_create()
            operation = True
        elif request.POST.get("comment_modify", None) is not None:
            comment_modify()
            operation = True
        elif request.POST.get("comment_delete", None) is not None:
            comment_delete()
            operation = True

    # others : open the website or refresh the website
    if not operation:
        article.views = article.views + 1
        article.save()
    return render(request, {"article": article, "comment": article.comments_set.all()})


def article_create(request):

    title = request.POST.get("title", None)
    author = request.session["username"]
    # author = request.POST.get("username", None)
    check_article = Article.objects.filter(title=title, author=author)
    if check_article is None:
        text = request.POST.get("title", None)
        article = Article(title=title, author=author, text=text)
        article.save()
        return HttpResponse("successfully create the article")
    else:
        return HttpResponse("has already existed")


def article_modify(request):

    # use session rather than "request.POST.get("author", None)" , 更可靠，防止他人更改网页，然后提交
    article = Article.objects.filter(title=request.POST.get("title", None), author=request.session["username"])
    if not article:
        return HttpResponse("No this article")

    text = request.POST.get("text", None)
    article.text = text
    article.save()


def article_delete(request):
    title = request.POST.get("title", None)
    author = request.session["username"]
    # author = request.POSt.get("username", None)
    article = Article.objects.filter(title=title, author=author)
    if article is not None:
        article.delete()
        return HttpResponse("successfully delete a article")
    else:
        return HttpResponse("no this article")

def user_article_show(request):
    pass
    # return

def user_comment_show(request):
    pass

# 要不要views， likes ： 添加User和Article的一对多关系

