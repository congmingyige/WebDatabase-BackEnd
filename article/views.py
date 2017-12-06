from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse
from django.core.urlresolvers import reverse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from article.models import Comment, Article
from user.models import User
import re
import json
from django.db.models import F

# Create your views here.
return_code = {
    'not_POST': 100,
    'user_not_existed': 103,
    'article_existed': 105,
    'article_not_existed': 106,
    'comment_existed': 107,
    'comment_not_existed': 108,

    'article_show_success': 120,
    'article_create_success': 121,
    'article_delete_success': 122,
    'article_update_success': 123,
    'article_liked_success': 124,
    'article_not_liked_success': 125,
    'article_user_show_success': 126,
    'comment_create_success': 127,
    'comment_delete_success': 128
}


# send title and text
def article_show(request, id_article):
    if request.method == 'POST':
        article = Article.objects.filter(id=id_article)
        if article:
            # choose not put 'comments' into article.values_list
            new_article = article.values_list('title', 'text')
            return HttpResponse(json.dumps(list(new_article), cls=Article.CJsonEncoder))
        # article not existed
        return HttpResponse(return_code['article_not_existed'], content_type="text/plain")
    # not a POST request
    return HttpResponse(return_code['not_POST'], content_type="text/plain")


# show article and corresponding comments
def article_comment_show(request, id_article):
    if request.method == 'POST':
        article = Article.objects.filter(id=id_article)
        if article:
            # choose not put 'comments' into article.values_list
            # new_article_comments = article[0].comments.all().values_list('id', 'author__phone', 'author__email', 'time', 'content')
            article_comments = article[0].comments.all()
            new_article_comments = []
            for new_comment in article_comments:
                dict_comment = {}
                dict_comment['id'] = new_comment.id
                if new_comment.author.phone is None:
                    dict_comment['author'] = new_comment.author.email
                else:
                    dict_comment['author'] = new_comment.author.phone
                dict_comment['time'] = new_comment.time
                dict_comment['content'] = new_comment.content
                new_article_comments.append(dict_comment)
            new_article = article.values_list('title', 'author__phone', 'author__email', 'time', 'text', 'views', 'liked')
            return HttpResponse(json.dumps({'article': list(new_article), 'article_comments': new_article_comments
                                            }, cls=Article.CJsonEncoder))
        # article not existed
        return HttpResponse(return_code['article_not_existed'], content_type="text/plain")
    # not a POST request
    return HttpResponse(return_code['not_POST'], content_type="text/plain")


# show some attributes of articles which published by a user
def author_article(request, id_user):
    if request.method == 'POST':
        author = User.objects.filter(id=id_user)
        if author:
            article = Article.objects.filter(author=id_user)
            new_article_comments = article[0].comments.all().values_list('id', 'author__phone', 'author__email', 'time', 'content')
            new_article = article.values_list('id', 'title', 'author__phone', 'author__email', 'time', 'text', 'views', 'liked')
            return HttpResponse(json.dumps({'article': list(new_article), 'article_comments': list(new_article_comments)
                                            }, cls=Article.CJsonEncoder))
        # user not existed
        return HttpResponse(return_code['user_not_existed'], content_type="text/plain")
    # not a POST request
    return HttpResponse(return_code['not_POST'], content_type="text/plain")


# moments of an author
def author_moments(request, id_author):
    if request.method == 'POST':
        author = User.objects.filter(id=id_author)
        if author:
            pass
    # not a POST request
    return HttpResponse(return_code['not_POST'], content_type="text/plain")


# create article
def article_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data['title']
        author = 1  # change!!!
        article = Article.objects.filter(title=title, author=author)
        if not article:
            Article.objects.create(title=title, author=User.objects.filter(id=author)[0], text=data['text'])
            return HttpResponse(return_code['article_create_success'], content_type="text/plain")
        # article existed
        return HttpResponse(return_code['article_existed'], content_type="text/plain")
    # not a POST request
    return HttpResponse(return_code['not_POST'], content_type="text/plain")


# update article
def article_update(request, id_article):
    if request.method == 'POST':
        article = Article.objects.filter(id=id_article)
        if article:
            data = json.loads(request.body)
            title = data['title']
            text = data['text']
            if not Article.objects.exclude(id=id_article).filter(title=title, author=1):    # change!!!
                article.update(title=title, text=text)
                return HttpResponse(return_code['article_update_success'], content_type="text/plain")
            return HttpResponse(return_code['article_existed'], content_type="text/plain")
        # article not existed
        return HttpResponse(return_code['article_not_existed'], content_type="text/plain")
    # not a POST request
    return HttpResponse(return_code['not_POST'], content_type="text/plain")


# delete article
def article_delete(request, id_article):
    if request.method == 'POST':
        article = Article.objects.filter(id=id_article)
        if article:
            article.delete()
            return HttpResponse(return_code['article_delete_success'], content_type="text/plain")
        # article not existed
        return HttpResponse(return_code['article_not_existed'], content_type="text/plain")
    # not a POST request
    return HttpResponse(return_code['not_POST'], content_type="text/plain")


# press the "liked" button in an article
def article_liked(request, id_article):
    if request.method == 'POST':
        article = Article.objects.filter(id=id_article)
        if article:
            article.update(liked=F('liked')+1)
            return HttpResponse(return_code['article_liked_success'], content_type="text/plain")
        # article not existed
        return HttpResponse(return_code['article_not_existed'], content_type="text/plain")
    # not a POST request
    return HttpResponse(return_code['not_POST'], content_type="text/plain")


# press the "not_liked" button in an article
def article_not_liked(request, id_article):
    if request.method == 'POST':
        article = Article.objects.filter(id=id_article)
        if article:
            article.update(liked=F('liked')-1)
            return HttpResponse(return_code['article_not_liked_success'], content_type="text/plain")
        # article not existed
        return HttpResponse(return_code['article_not_existed'], content_type="text/plain")
    # not a POST request
    return HttpResponse(return_code['not_POST'], content_type="text/plain")


# create comment
def comment_create(request, id_article):
    if request.method == 'POST':
        data = json.loads(request.body)
        article = Article.objects.filter(id=id_article)
        if article:
            author = User.objects.filter(id=1)  # change!!!
            content = data['content']
            comment = Comment(author=author[0], content=content)
            comment.save()
            article[0].comments.add(comment)
            comment.save()
            return HttpResponse(return_code['comment_create_success'], content_type="text/plain")
        # comment existed
        return HttpResponse(return_code['comment_existed'], content_type="text/plain")
    # not a POST request
    return HttpResponse(return_code['not_POST'], content_type="text/plain")


# delete comment
def comment_delete(request, id_comment):
    if request.method == 'POST':
        comment = Comment.objects.filter(comment=id_comment)
        if comment:
            comment.delete()
            return HttpResponse(return_code['comment_delete_success'], content_type="text/plain")
        # comment not existed
        return HttpResponse(return_code['comment_not_existed'], content_type="text/plain")
    # not a POST request
    return HttpResponse(return_code['not_POST'], content_type="text/plain")


def test():

    '''
    author = User.objects.filter(id=3)
    Comment.objects.create(author=author[0], content='haha')
    '''


    article = Article.objects.filter(id=1)
    comment = Comment.objects.filter(id=29)
    article[0].comments.add(comment[0])
    comment = Comment.objects.filter(id=30)
    article[0].comments.add(comment[0])
    comment = Comment.objects.filter(id=42)
    article[0].comments.add(comment[0])


    # return HttpResponse(json.dumps({'article': serializers.serialize("json", article)}))


    '''
    print(request.GET)
    print('ok')
    data = json.loads(request.body)
    print('ok')
    print(request.COOKIES)
    if 'username' in request.COOKIES:
        print(request.COOKIES['username'])
    else:
        print('no cookie')

    if 'username' in request.COOKIES:
        print(request.COOKIES['username'])
    response = render(request, "test.html", {"text": "hello world"})
    response.set_cookie("username", 'user', max_age=1800)
    return response
    '''


    '''
    print('ok')
    print(request.body)

    response = HttpResponse(json.dumps({'title': '1', 'author': '2', 'text': '3', 'comment': '4'}))
    # response = HttpResponse(json.dumps({'title': '1', 'author': '2', 'text': '3', 'comment': '4'}))
    response.set_cookie('username', 'user', max_age=1800)
    return response

    # return HttpResponse(json.dumps({'title': '1', 'author': '2', 'text': '3', 'comment': '4'}))
    # return HttpResponseRedirect('http://localhost:8080/', json.dumps({'title':'title', 'author':'2', 'context':'3', 'comment':'4'}))

    '''


'''
1.
.objects.get :
.all QuerySet, can use iterator
.get List : add []

2. In BackEnd :
    get messages : eval() : json(dict) -> str
    send messages : json.dumps() : json(dict) -> str
'''
