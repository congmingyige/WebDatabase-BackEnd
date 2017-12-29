from article.models import Comment, Article, Moment
from user.models import User
from django.shortcuts import HttpResponse
import json
from django.db.models import F
from django.contrib.sessions.backends.db import SessionStore
from collections import defaultdict
from django.core import serializers

# Create your views here.
return_code = {
    'not_POST': 100,
    'author_not_existed': 103,
    'article_existed': 105,
    'article_not_existed': 106,
    'comment_existed': 107,
    'comment_not_existed': 108,
    'no_authority': 109,
    'error': 110,

    'article_show_success': 120,
    'article_create_success': 121,
    'article_delete_success': 122,
    'article_update_success': 123,
    'article_liked_success': 124,
    'article_not_liked_success': 125,
    'article_comments_show_success': 126,
    'comment_create_success': 127,
    'article_collect_success': 128,
    'article_not_collection_success': 129
}
comments_round_count = 5


# show article and corresponding comments
def article_comments_show(request, id_article):
    session_key = request.META.get('HTTP_SESSIONKEY', None)
    session = SessionStore(session_key=session_key)
    if 'id_user' in session:
        id_user = session['id_user']
    else:
        id_user = 0

    if request.method == 'POST':
        article = Article.objects.filter(id=id_article)
        if article:
            article.update(views=F('views')+1)
            if article.filter(liked=id_user):
                if_liked = 1
            else:
                if_liked = 0
            if article.filter(collection=id_user):
                if_collection = 1
            else:
                if_collection = 0
            if article[0].author.id == id_user:
                if_modify = 1
            else:
                if_modify = 0
            article = article[0]

            article_comments = article.comments.all()
            new_article_comments = []
            for new_comment in article_comments:
                dict_comment = defaultdict(list)
                dict_comment['id'] = new_comment.id
                dict_comment['id_author'] = new_comment.author.id
                if new_comment.author.phone is None:
                    dict_comment['author'] = new_comment.author.email
                else:
                    dict_comment['author'] = new_comment.author.phone
                dict_comment['time'] = new_comment.time
                dict_comment['content'] = new_comment.content
                new_article_comments.append(dict_comment)

            new_article = defaultdict(list)
            new_article['title'] = article.title
            if article.author.phone is None:
                new_article['author'] = article.author.email
            else:
                new_article['author'] = article.author.phone
            new_article['time'] = article.time
            new_article['text'] = article.text
            new_article['views'] = article.views
            new_article['comments_count'] = article.comments_count
            new_article['liked_count'] = article.liked_count
            new_article['collection_count'] = article.collection_count

            return HttpResponse(json.dumps({'article': new_article,
                                            'article_comments': new_article_comments,
                                            'if_liked': if_liked,
                                            'if_collection': if_collection,
                                            'if_modify': if_modify,
                                            'sessionKey': session_key,
                                            'code': return_code['article_comments_show_success']}, cls=Article.CJsonEncoder))
        # article not existed
        return HttpResponse(json.dumps({'sessionKey': session_key,
                                        'code': return_code['article_not_existed']}))
    # not a POST request
    return HttpResponse(json.dumps({'sessionKey': session_key,
                                    'code': return_code['not_POST']}))


# show article
def article_show(request, id_article):
    session_key = request.META.get('HTTP_SESSIONKEY', None)
    session = SessionStore(session_key=session_key)
    if 'id_user' in session:
        id_user = session['id_user']
    else:
        id_user = 0

    if request.method == 'POST':
        article = Article.objects.filter(id=id_article)
        if article:
            article.update(views=F('views')+1)
            if article.filter(liked=id_user):
                if_liked = 1
            else:
                if_liked = 0
            if article.filter(collection=id_user):
                if_collection = 1
            else:
                if_collection = 0
            if article[0].author.id == id_user:
                if_modify = 1
            else:
                if_modify = 0
            article = article[0]

            new_article = defaultdict(list)
            new_article['title'] = article.title
            if article.author.phone is None:
                new_article['author'] = article.author.email
            else:
                new_article['author'] = article.author.phone
            new_article['time'] = article.time
            new_article['text'] = article.text
            new_article['views'] = article.views
            new_article['comments_count'] = article.comments_count
            new_article['liked_count'] = article.liked_count
            new_article['collection_count'] = article.collection_count

            return HttpResponse(json.dumps({'article': new_article,
                                            'if_liked': if_liked,
                                            'if_collection': if_collection,
                                            'if_modify': if_modify,
                                            'sessionKey': session_key,
                                            'code': return_code['article_comments_show_success']}, cls=Article.CJsonEncoder))
        # article not existed
        return HttpResponse(json.dumps({'sessionKey': session_key,
                                        'code': return_code['article_not_existed']}))
    # not a POST request
    return HttpResponse(json.dumps({'sessionKey': session_key,
                                    'code': return_code['not_POST']}))


# show article and corresponding comments
def comments_show(request, id_article):
    session_key = request.META.get('HTTP_SESSIONKEY', None)

    if request.method == 'POST':
        article = Article.objects.filter(id=id_article)
        if article:
            article = article[0]
            article_comments = article.comments.all()

            data = json.loads(request.body)
            comments_begin_number = data['comments_number']
            article_comments_count = len(article_comments)
            if comments_begin_number + comments_round_count <= article_comments_count:
                comments_number = comments_begin_number + comments_round_count
            else:
                comments_number = len(article_comments)

            print(article_comments_count)
            print(comments_begin_number)
            new_article_comments = []
            for index in range(article_comments_count-comments_begin_number-1, article_comments_count-comments_number-1, -1):
                new_comment = article_comments[index]
                dict_comment = defaultdict(list)
                dict_comment['id'] = new_comment.id
                dict_comment['id_author'] = new_comment.author.id
                if new_comment.author.phone is None:
                    dict_comment['author'] = new_comment.author.email
                else:
                    dict_comment['author'] = new_comment.author.phone
                dict_comment['time'] = new_comment.time
                dict_comment['content'] = new_comment.content
                new_article_comments.append(dict_comment)

            return HttpResponse(json.dumps({'article_comments': new_article_comments,
                                            'comments_number': comments_number,
                                            'sessionKey': session_key,
                                            'code': return_code['article_comments_show_success']}, cls=Article.CJsonEncoder))
        # article not existed
        return HttpResponse(json.dumps({'sessionKey': session_key,
                                        'code': return_code['article_not_existed']}))
    # not a POST request
    return HttpResponse(json.dumps({'sessionKey': session_key,
                                    'code': return_code['not_POST']}))


# send title and text of an article for the updating of the article
def article_title_text(request, id_article):
    session_key = request.META.get('HTTP_SESSIONKEY', None)

    if request.method == 'POST':
        article = Article.objects.filter(id=id_article)
        if article:
            return HttpResponse(json.dumps({'title': article[0].title,
                                            'text': article[0].text}, cls=Article.CJsonEncoder))
        # article not existed
        return HttpResponse(json.dumps({'sessionKey': session_key,
                                        'code': return_code['article_not_existed']}))
    # not a POST request
    return HttpResponse(json.dumps({'sessionKey': session_key,
                                    'code': return_code['not_POST']}))


# create article
def article_create(request):
    session_key = request.META.get('HTTP_SESSIONKEY', None)
    session = SessionStore(session_key=session_key)
    if 'id_user' in session:
        id_user = session['id_user']
    else:
        return HttpResponse(json.dumps({'sessionKey': session_key,
                                        'code': return_code['author_not_existed']}))

    if request.method == 'POST':
        data = json.loads(request.body)
        title = data['title']
        article = Article.objects.filter(title=title, author=id_user)
        if not article:
            Article.objects.create(title=title, author=User.objects.filter(id=id_user)[0], text=data['text'])
            return HttpResponse(json.dumps({'sessionKey': session_key,
                                            'code': return_code['article_create_success']}))
        # article existed
        return HttpResponse(json.dumps({'sessionKey': session_key,
                                        'code': return_code['article_existed']}))
    # not a POST request
    return HttpResponse(json.dumps({'sessionKey': session_key,
                                    'code': return_code['not_POST']}))


# update article
def article_update(request, id_article):
    session_key = request.META.get('HTTP_SESSIONKEY', None)
    session = SessionStore(session_key=session_key)
    if 'id_user' in session:
        id_user = session['id_user']
    else:
        return HttpResponse(json.dumps({'sessionKey': session_key,
                                        'code': return_code['author_not_existed']}))

    if request.method == 'POST':
        article = Article.objects.filter(id=id_article)
        if article:
            if article[0].author.id == id_user:
                data = json.loads(request.body)
                title = data['title']
                text = data['text']
                if not Article.objects.exclude(id=id_article).filter(title=title, author=id_user):
                    article.update(title=title, text=text)
                    return HttpResponse(json.dumps({'sessionKey': session_key,
                                                    'code': return_code['article_update_success']}))
                # article existed
                return HttpResponse(json.dumps({'sessionKey': session_key,
                                                'code': return_code['article_existed']}))
            # no authority
            return HttpResponse(json.dumps({'sessionKey': session_key,
                                            'code': return_code['no_authority']}))
        # article not existed
        return HttpResponse(json.dumps({'sessionKey': session_key,
                                        'code': return_code['article_not_existed']}))
    # not a POST request
    return HttpResponse(json.dumps({'sessionKey': session_key,
                                    'code': return_code['not_POST']}))


# delete article
def article_delete(request, id_article):
    session_key = request.META.get('HTTP_SESSIONKEY', None)
    session = SessionStore(session_key=session_key)
    if 'id_user' in session:
        id_user = session['id_user']
    else:
        return HttpResponse(json.dumps({'sessionKey': session_key,
                                        'code': return_code['author_not_existed']}))

    if request.method == 'POST':
        article = Article.objects.filter(id=id_article)
        if article:
            if article[0].author.id == id_user:
                article.delete()
                return HttpResponse(json.dumps({'sessionKey': session_key,
                                                'code': return_code['article_delete_success']}))
            # no authority
            return HttpResponse(json.dumps({'sessionKey': session_key,
                                            'code': return_code['no_authority']}))
        # article not existed
        return HttpResponse(json.dumps({'sessionKey': session_key,
                                        'code': return_code['article_not_existed']}))
    # not a POST request
    return HttpResponse(json.dumps({'sessionKey': session_key,
                                    'code': return_code['not_POST']}))


# a user likes an article
def article_liked(request, id_article):
    session_key = request.META.get('HTTP_SESSIONKEY', None)
    session = SessionStore(session_key=session_key)
    if 'id_user' in session:
        id_user = session['id_user']
    else:
        return HttpResponse(json.dumps({'sessionKey': session_key,
                                        'code': return_code['author_not_existed']}))

    if request.method == 'POST':
        article = Article.objects.filter(id=id_article)
        if article:
            if not article.filter(liked=id_user):
                article.update(liked_count=F('liked_count') + 1)
                article[0].liked.add(id_user)
                return HttpResponse(json.dumps({'sessionKey': session_key,
                                                'code': return_code['article_liked_success']}))
            # error
            return HttpResponse(json.dumps({'sessionKey': session_key,
                                            'code': return_code['error']}))
        # article not existed
        return HttpResponse(json.dumps({'sessionKey': session_key,
                                        'code': return_code['article_not_existed']}))
    # not a POST request
    return HttpResponse(json.dumps({'sessionKey': session_key,
                                    'code': return_code['not_POST']}))


# cancel : a user likes an article
def article_not_liked(request, id_article):
    session_key = request.META.get('HTTP_SESSIONKEY', None)
    session = SessionStore(session_key=session_key)
    if 'id_user' in session:
        id_user = session['id_user']
    else:
        return HttpResponse(json.dumps({'sessionKey': session_key,
                                        'code': return_code['author_not_existed']}))

    if request.method == 'POST':
        article = Article.objects.filter(id=id_article)
        if article:
            if article.filter(liked=id_user):
                article.update(liked_count=F('liked_count') - 1)
                article[0].liked.remove(id_user)
                return HttpResponse(json.dumps({'sessionKey': session_key,
                                                'code': return_code['article_not_liked_success']}))
            # error
            return HttpResponse(json.dumps({'sessionKey': session_key,
                                            'code': return_code['error']}))
        # article not existed
        return HttpResponse(json.dumps({'sessionKey': session_key,
                                        'code': return_code['article_not_existed']}))
    # not a POST request
    return HttpResponse(json.dumps({'sessionKey': session_key,
                                    'code': return_code['not_POST']}))


# a user collects an article
def article_collection(request, id_article):
    session_key = request.META.get('HTTP_SESSIONKEY', None)
    session = SessionStore(session_key=session_key)
    if 'id_user' in session:
        id_user = session['id_user']
    else:
        return HttpResponse(json.dumps({'sessionKey': session_key,
                                        'code': return_code['author_not_existed']}))

    if request.method == 'POST':
        article = Article.objects.filter(id=id_article)
        if article:
            if not article.filter(collection=id_user):
                article.update(collection_count=F('collection_count') + 1)
                article[0].collection.add(id_user)
                return HttpResponse(json.dumps({'sessionKey': session_key,
                                                'code': return_code['article_collect_success']}))
            # error
            return HttpResponse(json.dumps({'sessionKey': session_key,
                                            'code': return_code['error']}))
        # article not existed
        return HttpResponse(json.dumps({'sessionKey': session_key,
                                        'code': return_code['article_not_existed']}))
    # not a POST request
    return HttpResponse(json.dumps({'sessionKey': session_key,
                                    'code': return_code['not_POST']}))


# cancel : a user collects an article
def article_not_collection(request, id_article):
    session_key = request.META.get('HTTP_SESSIONKEY', None)
    session = SessionStore(session_key=session_key)
    if 'id_user' in session:
        id_user = session['id_user']
    else:
        return HttpResponse(json.dumps({'sessionKey': session_key,
                                        'code': return_code['author_not_existed']}))

    if request.method == 'POST':
        article = Article.objects.filter(id=id_article)
        if article:
            if article.filter(collection=id_user):
                article.update(collection_count=F('collection_count') - 1)
                article[0].collection.remove(id_user)
                return HttpResponse(json.dumps({'sessionKey': session_key,
                                                'code': return_code['article_not_collection_success']}))
            # error
            return HttpResponse(json.dumps({'sessionKey': session_key,
                                            'code': return_code['error']}))
        # article not existed
        return HttpResponse(json.dumps({'sessionKey': session_key,
                                        'code': return_code['article_not_existed']}))
    # not a POST request
    return HttpResponse(json.dumps({'sessionKey': session_key,
                                    'code': return_code['not_POST']}))


# a user publishes a comment
def comment_create(request, id_article):
    session_key = request.META.get('HTTP_SESSIONKEY', None)
    session = SessionStore(session_key=session_key)
    if 'id_user' in session:
        id_user = session['id_user']
    else:
        return HttpResponse(json.dumps({'sessionKey': session_key,
                                        'code': return_code['author_not_existed']}))

    if request.method == 'POST':
        article = Article.objects.filter(id=id_article)
        if article:
            data = json.loads(request.body)
            content = data['content']
            author = User.objects.filter(id=id_user)
            comment = Comment(author=author[0], content=content)
            comment.save()
            article[0].comments.add(comment)
            article.update(comments_count=F('comments_count')+1)
            return HttpResponse(json.dumps({'sessionKey': session_key,
                                            'id': comment.id,
                                            'time': comment.time,
                                            'code': return_code['comment_create_success']}, cls=Article.CJsonEncoder))
        # article not existed
        return HttpResponse(json.dumps({'sessionKey': session_key,
                                        'code': return_code['article_not_existed']}))
    # not a POST request
    return HttpResponse(json.dumps({'sessionKey': session_key,
                                    'code': return_code['not_POST']}))


# delete comment
def comment_delete(request, id_article, id_comment):
    session_key = request.META.get('HTTP_SESSIONKEY', None)
    session = SessionStore(session_key=session_key)
    if 'id_user' in session:
        id_user = session['id_user']
    else:
        return HttpResponse(json.dumps({'sessionKey': session_key,
                                        'code': return_code['author_not_existed']}))

    if request.method == 'POST':
        comment = Comment.objects.filter(id=id_comment)
        if comment:
            if comment[0].author.id == id_user:
                comment[0].delete()
                article = Article.objects.filter(id=id_article)
                article.update(comments_count=F('comments_count')-1)
                return HttpResponse(json.dumps({'sessionKey': session_key,
                                                'code': return_code['comment_delete_success']}))
            # no authority
            return HttpResponse(json.dumps({'sessionKey': session_key,
                                            'code': return_code['no_authority']}))
        # comment not existed
        return HttpResponse(json.dumps({'sessionKey': session_key,
                                        'code': return_code['comment_not_existed']}))
    # not a POST request
    return HttpResponse(json.dumps({'sessionKey': session_key,
                                    'code': return_code['not_POST']}))


# articles which published by an author
def author_article(request, id_author):
    session_key = request.META.get('HTTP_SESSIONKEY', None)

    if request.method == 'POST':
        author = User.objects.filter(id=id_author)
        if author:
            article = Article.objects.filter(author=id_author)

            new_article = []
            for article_s in article:
                dict_article = defaultdict(list)
                dict_article['id'] = article_s.id
                dict_article['title'] = article_s.title
                dict_article['id_author'] = article_s.author.id
                if article_s.author.phone is None:
                    dict_article['author'] = article_s.author.email
                else:
                    dict_article['author'] = article_s.author.phone
                dict_article['time'] = article_s.time
                dict_article['text'] = article_s.text
                dict_article['views'] = article_s.views
                dict_article['comments_count'] = article_s.comments_count
                dict_article['liked_count'] = article_s.liked_count
                dict_article['collection_count'] = article_s.collection_count
                new_article.append(dict_article)

            return HttpResponse(json.dumps({'article': new_article,
                                            'sessionKey': session_key,
                                            'code': return_code['article_comments_show_success']}, cls=Article.CJsonEncoder))
        # author not existed
        return HttpResponse(json.dumps({'sessionKey': session_key,
                                        'code': return_code['author_not_existed']}))
    # not a POST request
    return HttpResponse(json.dumps({'sessionKey': session_key,
                                    'code': return_code['not_POST']}))


# articles which an author like
def author_article_liked(request, id_author):
    session_key = request.META.get('HTTP_SESSIONKEY', None)

    if request.method == 'POST':
        author = User.objects.filter(id=id_author)
        if author:
            article = Article.objects.filter(liked=id_author)
            new_article = []
            for article_s in article:
                dict_article = defaultdict(list)
                dict_article['id'] = article_s.id
                dict_article['title'] = article_s.title
                dict_article['id_author'] = article_s.author.id
                if article_s.author.phone is None:
                    dict_article['author'] = article_s.author.email
                else:
                    dict_article['author'] = article_s.author.phone
                new_article.append(dict_article)

            return HttpResponse(json.dumps({'article': new_article,
                                            'sessionKey': session_key,
                                            'code': return_code['article_comments_show_success']}, cls=Article.CJsonEncoder))
        # author not existed
        return HttpResponse(json.dumps({'sessionKey': session_key,
                                        'code': return_code['author_not_existed']}))
    # not a POST request
    return HttpResponse(json.dumps({'sessionKey': session_key,
                                    'code': return_code['not_POST']}))


# articles which an author collect
def author_article_collection(request, id_author):
    session_key = request.META.get('HTTP_SESSIONKEY', None)

    if request.method == 'POST':
        author = User.objects.filter(id=id_author)
        if author:
            article = Article.objects.filter(collection=id_author)
            new_article = []
            for article_s in article:
                dict_article = defaultdict(list)
                dict_article['id'] = article_s.id
                dict_article['title'] = article_s.title
                dict_article['id_author'] = article_s.author.id
                if article_s.author.phone is None:
                    dict_article['author'] = article_s.author.email
                else:
                    dict_article['author'] = article_s.author.phone
                new_article.append(dict_article)

            if author[0].phone is None:
                author_name = author[0].email
            else:
                author_name = author[0].phone
            return HttpResponse(json.dumps({'author_name': author_name,
                                            'article': new_article,
                                            'sessionKey': session_key,
                                            'code': return_code['article_comments_show_success']}, cls=Article.CJsonEncoder))
        # author not existed
        return HttpResponse(json.dumps({'sessionKey': session_key,
                                        'code': return_code['author_not_existed']}))
    # not a POST request
    return HttpResponse(json.dumps({'sessionKey': session_key,
                                    'code': return_code['not_POST']}))


# articles which an author publishes comment
def author_article_comment(request, id_author):
    session_key = request.META.get('HTTP_SESSIONKEY', None)

    if request.method == 'POST':
        author = User.objects.filter(id=id_author)
        if author:
            article = Article.objects.filter(comments=id_author)

            new_article = []
            for article_s in article:
                dict_article = defaultdict(list)
                dict_article['id'] = article_s.id
                dict_article['title'] = article_s.title
                dict_article['id_author'] = article_s.author.id
                if article_s.author.phone is None:
                    dict_article['author'] = article_s.author.email
                else:
                    dict_article['author'] = article_s.author.phone
                new_article.append(dict_article)

            return HttpResponse(json.dumps({'article': new_article,
                                            'sessionKey': session_key,
                                            'code': return_code['article_comments_show_success']}, cls=Article.CJsonEncoder))
        # author not existed
        return HttpResponse(json.dumps({'sessionKey': session_key,
                                        'code': return_code['author_not_existed']}))
    # not a POST request
    return HttpResponse(json.dumps({'sessionKey': session_key,
                                    'code': return_code['not_POST']}))


# moments of an author
def author_moments(request, id_author):
    session_key = request.META.get('HTTP_SESSIONKEY', None)

    if request.method == 'POST':
        author = User.objects.filter(id=id_author)
        if author:
            pass
    # not a POST request
    return HttpResponse(json.dumps({'sessionKey': session_key,
                                    'code': return_code['not_POST']}))


def test(request):
    if request.method == 'POST':
        article = Article.objects.filter(id=2)
        if article:
            print(article[0])
            if article.filter(id=1) is not None:
                print('ok1')

            if article.filter(collection=1):
                print('ok')

'''
1.
.objects.get :
.all QuerySet, can use iterator
.get List : add []

2.
In BackEnd :
    get messages : eval() : json(dict) -> str
    send messages : json.dumps() : json(dict) -> str

3.
new_article = article.values_list('title', 'author__phone', 'author__email', 'time', 'text', 'views', 'liked')

4.
    print(request.GET)
    print(request.COOKIES)
    if 'username' in request.COOKIES:
        print(request.COOKIES['username'])
    else:
        print('no cookie')
    response.set_cookie("username", 'user', max_age=1800)

5.
    response = render(request, "test.html", {"text": "hello world"})
    return response
    return HttpResponse(json.dumps({'article': serializers.serialize("json", article)}))
    return HttpResponseRedirect('http://localhost:8080/', json.dumps({'title':'', 'author':'', 'context':'', 'comment':''}))
    
6.
        if id_user != id_author:
            return HttpResponse(json.dumps({'sessionKey': session_key,
                                            'code': return_code['no_authority']}))
'''
