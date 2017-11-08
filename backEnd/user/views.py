from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from user.models import User
from backEnd import urls
import re

account_code = {
    "not_POST": 100,
    "username_invalid": 101,
    "password_invalid": 102,
    "username_existed": 103,  #for register
    "username_not_exist": 105,  #for login
    "password_error": 106,
    "register_success": 110,
    "login_success": 120,
    "reset_password_success": 130,
    "logout_success": 140
}


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
        #   get username and password from POST request
        username = request.POST.get('username')
        pwd = request.POST.get('password')

        #   judge phone number or e-mail address, then check the validity of username
        if "@" in username:
            at_existed = True
            pattern = re.compile(r"^[-_\w\.]{0,64}@([-\w]{1,63}\.)*[-\w]{1,63}$")
        else:
            at_existed = False
            pattern = re.compile(r"^\d{11}$")
        if re.match(pattern, username) is None:
            return HttpResponse(account_code['username_invalid'], content_type="text/plain")
        #   check the validity of password
        if not 6 <= len(pwd) <= 64:
            return HttpResponse(account_code['password_invalid'], content_type="text/plain")

        #   check up whether the account has existed
        if at_existed:
            new_user = User.objects.filter(email=username)
        else:
            new_user = User.objects.filter(phone=username)
        if new_user:
            return HttpResponse(account_code['username_existed'], content_type="text/plain")
        else:
            #   create a new user in the database
            if at_existed:
                User.objects.create(email=username, password=pwd)
            else:
                User.objects.create(phone=username, password=pwd)

        response = HttpResponse(account_code['register_success'], content_type="text/plain")
        response.set_cookie("username", username, max_age=1800)
        return response
    #   not a POST request
    return HttpResponse(account_code['not_POST'], content_type="text/plain")


'''
2.//登陆
  账号存在检测[注意账号类别]
  密码匹配
  异常捕获
  返回登陆信息
'''
def login(request):
    if request.method == 'POST':
        #   get username and password from POST request
        username = request.POST.get('username')
        pwd = request.POST.get('password')

        #   judge phone number or e-mail address, then check the validity of username
        if "@" in username:
            at_existed = True
            pattern = re.compile(r"^[-_\w\.]{0,64}@([-\w]{1,63}\.)*[-\w]{1,63}$")
        else:
            at_existed = False
            pattern = re.compile(r"^\d{11}$")
        if re.match(pattern, username) is None:
            return HttpResponse(account_code['username_invalid'], content_type="text/plain")
        #   check the validity of password
        if not 6 <= len(pwd) <= 64:
            return HttpResponse(account_code['password_invalid'], content_type="text/plain")

        #   check up whether the account has existed
        if at_existed:
            new_user = User.objects.filter(email=username)
        else:
            new_user = User.objects.filter(phone=username)
        if not new_user:
            return HttpResponse(account_code['username_not_exist'], content_type="text/plain")
        else:
            if new_user[0].password != pwd:
                return HttpResponse(account_code['password_error'], content_type="text/plain")

        response = HttpResponse(account_code['login_success'], content_type="text/plain")
        response.set_cookie("username", username, max_age=1800)
        return response
    #   not a POST request

    return HttpResponse(account_code['not_POST'], content_type="text/plain")


'''
 3.//忘记密码
   与注册账号类似
'''
def password_forget(request):
    if request.method == 'POST':
        #   get username and password from POST request
        username = request.POST.get('username')
        pwd = request.POST.get('password')

        #   judge phone number or e-mail address, then check the validity of username
        if "@" in username:
            at_existed = True
            pattern = re.compile(r"^[-_\w\.]{0,64}@([-\w]{1,63}\.)*[-\w]{1,63}$")
        else:
            at_existed = False
            pattern = re.compile(r"^\d{11}$")
        if re.match(pattern, username) is None:
            return HttpResponse(account_code['username_invalid'], content_type="text/plain")
        #   check the validity of password
        if not 6 <= len(pwd) <= 64:
            return HttpResponse(account_code['password_invalid'], content_type="text/plain")

        #   check up whether the account has existed
        if at_existed:
            new_user = User.objects.filter(email=username)
        else:
            new_user = User.objects.filter(phone=username)
        if not new_user:
            return HttpResponse(account_code['username_not_exist'], content_type="text/plain")
        else:
            #   update the password
            new_user.update(password=pwd)

        response = HttpResponse(account_code['reset_password_success'], content_type="text/plain")
        response.set_cookie("username", username, max_age=1800)
        return response
    #   not a POST request
    return HttpResponse(account_code['not_POST'], content_type="text/plain")


'''
  4.登出功能
  移除用户的Cookies
'''
def logout(request):
    if request.method == 'POST':
        response = HttpResponse(account_code['logout_success'], content_type="text/plain")
        response.delete_cookie('username')
        return response



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
