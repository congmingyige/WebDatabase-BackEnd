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
#from user import views
from user.views import login,register,password_forget,main_page

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'login/', login),
    url(r'register/', register),
    url(r'password_forget/', password_forget),
    url(r'main_page/', main_page, name='main_page')
]

'''
in setting.py:

重启web服务时，会出错，因为django有一个跨站请求保护机制，我们在settings文件中将它关闭。
Line 47 : #'django.middleware.csrf.CsrfViewMiddleware',

CSS,JS和各种插件的位置
Line 124~126

'''
