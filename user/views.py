from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import HttpResponse
from django.core.urlresolvers import reverse
from user.models import User
from backEnd import urls
import re

# Test in tests.py

account_feedback = {
        "username_blank":       "Please input username",
        "password_blank":       "Please input password",
        "username_exist":       "username has existed",
        "username_non-existent": "username has not existed",
        "username_wrong":       "Wrong username, it is neither phone nor email",
        "password_wrong":       "Wrong password, the length of password must be not less than 6 and not more than 64",
        "account_wrong":        "username or password wrong"
}

account_mode = {
        "register":         "register",
        "login":            "login",
        "password_forget": "password_forget"
}


'''
To add:
1.Verify:judge whether machines or human do the operation
2.Send identifying code to phone / email, when is to register or change password
'''

'''
efficiency:
1.use "is" is faster than "=="
2.use "if x is not None" is better than "if not x is None"
2.use "if ... in ..." : faster
'''

'''
return value:
1. re.match: None or others
2. .objects.filter: [] or others
3. request.POST.get("x", y): y or others
'''

'''
1.//注册账号
  账号重名检测[注意账号类别]
  数据有效性、规范检测
  异常捕获
  存入数据库中
  返回登录信息
'''


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        pwd = request.POST.get('password', None)

        if username is None or pwd is None:
            return render(request, "account.html", {"info": "", "mode": account_mode["register"]})
        if username == "":
            return render(request, "account.html", {"info": account_feedback["username_blank"], "mode": account_mode["register"]})
        if pwd == "":
            return render(request, "account.html", {"info": account_feedback["password_blank"], "mode": account_mode["register"]})

        pos_at = True if ("@" in username) else False
        if not pos_at and re.match(r"^((13[0-9])|(15[^4])|(18[0,2,3,5-9])|(17[0-8])|(147))\d{8}$", username) is None \
                or pos_at and re.match(r"^[-_\w\.]{0,64}@([-\w]{1,63}\.)*[-\w]{1,63}$", username) is None:
            return render(request, "account.html", {"info": account_feedback["username_wrong"], "mode": account_mode["register"]})

        if not 6 <= len(pwd) <= 64:
            return render(request, "account.html", {"info": account_feedback["password_wrong"], "mode": account_mode["register"]})

        if not pos_at and User.objects.filter(phone=username) \
                or pos_at and User.objects.filter(email=username):
            return render(request, "account.html", {"info": account_feedback["username_exist"], "mode": account_mode["register"]})

        # 验证信息发送到phone/email，等待核实

        if pos_at:
            User.objects.create(email=username, password=pwd)
        else:
            User.objects.create(phone=username, password=pwd)

        response = HttpResponseRedirect(reverse("main_page"))
        response.set_cookie("username", username)
        return response

    return render(request, "account.html", {"info": "", "mode": account_mode["register"]})


'''
2.//登陆
  账号存在检测[注意账号类别]
  密码匹配
  异常捕获
  返回登陆信息
'''


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username", None)
        pwd = request.POST.get("password", None)

        if username is None or pwd is None:
            return render(request, "account.html", {"info": "", "mode": account_mode["login"]})
        if username == "":
            return render(request, "account.html", {"info": account_feedback["username_blank"], "mode": account_mode["login"]})
        if pwd == "":
            return render(request, "account.html", {"info": account_feedback["password_blank"], "mode": account_mode["login"]})

        pos_at = True if ("@" in username) else False
        if not pos_at and re.match(r"^((13[0-9])|(15[^4])|(18[0,2,3,5-9])|(17[0-8])|(147))\d{8}$", username) is None \
                or pos_at and re.match(r"^[-_\w\.]{0,64}@([-\w]{1,63}\.)*[-\w]{1,63}$", username) is None:
            return render(request, "account.html", {"info": account_feedback["username_wrong"], "mode": account_mode["login"]})

        if not 6 <= len(pwd) <= 64:
            return render(request, "account.html", {"info": account_feedback["password_wrong"], "mode": account_mode["login"]})

        if not pos_at and User.objects.filter(phone=username, password=pwd) \
                or pos_at and User.objects.filter(email=username, password=pwd):
            # admin 页面
            if username == "1@qq.com":
                user_list = User.objects.all()
                return render(request, "account_show.html", {"data": user_list})

            response = HttpResponseRedirect(reverse("main_page"))
            response.set_cookie("username", username)
            return response
        else:
            return render(request, "account.html", {"info": account_feedback["account_wrong"], "mode": account_mode["login"]})

    return render(request, "account.html", {"info": "", "mode": account_mode["login"]})


'''
 3.//忘记密码
   与注册账号类似
'''


def password_forget(request):
    if request.method == 'POST':
        username = request.POST.get("username", None)
        pwd = request.POST.get("password", None)

        if username is None or pwd is None:
            return render(request, "account.html", {"info": "", "mode": account_mode["password_forget"]})
        if username == "":
            return render(request, "account.html", {"info": account_feedback["username_blank"], "mode": account_mode["password_forget"]})
        if pwd == "":
            return render(request, "account.html", {"info": account_feedback["password_blank"], "mode": account_mode["password_forget"]})

        pos_at = True if ("@" in username) else False
        if not pos_at and re.match(r"^((13[0-9])|(15[^4])|(18[0,2,3,5-9])|(17[0-8])|(147))\d{8}$", username) is None \
                or pos_at and re.match(r"^[-_\w\.]{0,64}@([-\w]{1,63}\.)*[-\w]{1,63}$", username) is None:
            return render(request, "account.html", {"info": account_feedback["username_wrong"], "mode": account_mode["password_forget"]})

        if not 6 <= len(pwd) <= 64:
            return render(request, "account.html", {"info": account_feedback["password_wrong"], "mode": account_mode["password_forget"]})

        if not pos_at and not User.objects.filter(phone=username) \
                or pos_at and not User.objects.filter(email=username):
            return render(request, "account.html", {"info": account_feedback["username_non-existent"], "mode": account_mode["password_forget"]})

        # 验证信息发送到phone/email，等待核实

        if pos_at:
            User.objects.filter(email=username).update(password=pwd)
        else:
            User.objects.filter(phone=username).update(password=pwd)

        response = HttpResponseRedirect(reverse("main_page"))
        response.set_cookie("username", username)
        return response

    return render(request, "account.html", {"info": "", "mode": account_mode["password_forget"]})


'''
 4.//与前端vue.js 的表单功能结合
   探讨如何将网页表单数据传送到后端
   Django中的视图中，方法接收到的request对象有什么成员属性?如何利用?
   (使用vue.js的form 还是 Django的form 或者是其它解决方案?)
'''


def main_page(request):
    return render(request, "main_page.html", {"username": request.COOKIES["username"]})
