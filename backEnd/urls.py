"""backEnd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
#from django.contrib import admin
from user.views import login, register, password_forget, logout, editProfile, getProfile
from article.views import  article_comments_show, article_show, comments_show,\
        article_create, article_title_text, article_update, article_delete,\
        article_liked, article_not_liked, article_collection, article_not_collection, comment_create, comment_delete, \
        author_article, author_article_liked, author_article_collection, author_article_comment, author_moments, test

# 从上到下识别，如果识别成功，下面的就不用再识别
urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^login/?', login),
    url(r'^register/?', register),
    url(r'^password_forget/?', password_forget),
    url(r'^logout/?', logout),

    url(r'^p/create/?', article_create),
    url(r'^p/(\d+)/article_title_text/?', article_title_text),
    url(r'^p/(\d+)/update/?', article_update),
    url(r'^p/(\d+)/delete/?', article_delete),

    url(r'^p/(\d+)/liked/?', article_liked),
    url(r'^p/(\d+)/not_liked/?', article_not_liked),
    url(r'^p/(\d+)/collection/?', article_collection),
    url(r'^p/(\d+)/not_collection/?', article_not_collection),
    url(r'^p/(\d+)/c/create/?', comment_create),
    url(r'^p/(\d+)/c/(\d+)/delete/?', comment_delete),

    url(r'^p/(\d+)/article/?', article_show),
    url(r'^p/(\d+)/comments/?', comments_show),
    url(r'^p/(\d+)/?', article_comments_show),

    url(r'^a/(\d+)/article/?', author_article),
    url(r'^a/(\d+)/liked/?', author_article_liked),
    url(r'^a/(\d+)/collection/?', author_article_collection),
    url(r'^a/(\d+)/comment/?', author_article_comment),
    url(r'^a/(\d+)/moments/?', author_moments),
    url(r'^a/(\d+)/editProfile/?', editProfile),
    url(r'^a/(\d+)/getProfile/?', getProfile),

    url(r'test', test)
]

'''
setting.py:

1.
app生成后
INSTALLED_APPS 要加app名：user，article

2.
重启web服务时，会出错，因为django有一个跨站请求保护机制，我们在settings文件中将它关闭。
Line 47 : #'django.middleware.csrf.CsrfViewMiddleware',

3.
CSS,JS和各种插件的位置
Line 124~126

4.
前端传送headers到后端，headers的变量在CORS_ALLOW_HEADERS定义

'''
