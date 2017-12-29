
from user.models import User
from django.shortcuts import HttpResponse
import re
import json
from django.contrib.sessions.backends.db import SessionStore

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
    "logout_success": 140,
    "logout_error": 141,
    "options_request": 150,
    "editProfile_success": 160,
    "getProfile_success": 170
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
        post = json.loads(request.body)
        username = post['username']
        pwd = post['password']

        #   judge phone number or e-mail address, then check the validity of username
        if "@" in username:
            at_existed = True
            pattern = re.compile(r"^[-_\w\.]{0,64}@([-\w]{1,63}\.)*[-\w]{1,63}$")
        else:
            at_existed = False
            pattern = re.compile(r"^\d{11}$")
        if re.match(pattern, username) is None:
            return HttpResponse(json.dumps({
                                   'code':account_code['username_invalid'],
                                   'sessionKey': ''
                            }),content_type="text/plain")
        #   check the validity of password
        if not 6 <= len(pwd) <= 64:
            return HttpResponse(json.dumps({
                                   'code':account_code['password_invalid'],
                                   'sessionKey': ''
                            }),content_type="text/plain")

        #   check up whether the account has existed
        if at_existed:
            new_user = User.objects.filter(email=username)
        else:
            new_user = User.objects.filter(phone=username)
        if new_user:
            return HttpResponse(json.dumps({
                                   'code':account_code['username_existed'],
                                   'sessionKey': ''
                            }),content_type="text/plain")
        else:
            #   create a new user in the database
            if at_existed:
                new_user = User(email=username, password=pwd)
                new_user.save()
            else:
                new_user = User(phone=username, password=pwd)
                new_user.save()

        session = SessionStore()
        session['username'] = username
        session['id_user'] = new_user.id
        session.save()

        return HttpResponse(json.dumps({
                                   'id_user': new_user.id,
                                   'code':account_code['register_success'],
                                   'sessionKey': ''
                            }),content_type="text/plain")
    #   not a POST request
    elif request.method == 'OPTIONS':
        response = HttpResponse(json.dumps({
                                   'code':account_code['options_request'],
                                   'sessionKey': ''
                            }),content_type="text/plain")
        response['Access-Control-Allow-Origin'] = "*"
        return response
    else:
        return HttpResponse(json.dumps({
                                   'code':account_code['not_POST'],
                                   'sessionKey': ''
                            }),content_type="text/plain")


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
        post = json.loads(request.body)
        username = post['username']
        pwd = post['password']

        #   judge phone number or e-mail address, then check the validity of username
        if "@" in username:
            at_existed = True
            pattern = re.compile(r"^[-_\w\.]{0,64}@([-\w]{1,63}\.)*[-\w]{1,63}$")
        else:
            at_existed = False
            pattern = re.compile(r"^\d{11}$")
        if re.match(pattern, username) is None:
            return HttpResponse(json.dumps({
                                   'code':account_code['username_invalid'],
                                   'sessionKey': ''
                                }),content_type="text/plain")
        #   check the validity of password
        if not 6 <= len(pwd) <= 64:
            return HttpResponse(json.dumps({
                                   'code':account_code['password_invalid'],
                                   'sessionKey': ''
                                }),content_type="text/plain")

        #   check up whether the account has existed
        if at_existed:
            new_user = User.objects.filter(email=username)
        else:
            new_user = User.objects.filter(phone=username)
        if not new_user:
            return HttpResponse(json.dumps({
                                   'code':account_code['username_not_exist'],
                                   'sessionKey': ''
                                }),content_type="text/plain")
        else:
            if new_user[0].password != pwd:
                return HttpResponse(json.dumps({
                                   'code':account_code['password_error'],
                                   'sessionKey': ''
                                }),content_type="text/plain")
        #   create a session
        s = SessionStore()
        s['username'] = username
        s['id_user'] = new_user[0].id
        s.save()
        response = HttpResponse(json.dumps({
                                   'id_user': new_user[0].id,
                                   'code':account_code['login_success'],
                                   'sessionKey': s.session_key,
                                   'username': username
                                }),content_type="text/plain")
        return response

    #   not a POST request
    elif request.method == 'OPTIONS':
        response = HttpResponse(json.dumps({
                                   'code':account_code['options_request'],
                                   'sessionKey': ''
                                }),content_type="text/plain")
        response['Access-Control-Allow-Origin'] = "*"
        return response
    else:
        return HttpResponse(json.dumps({
                                   'code':account_code['not_POST'],
                                   'sessionKey': ''
                            }),content_type="text/plain")


'''
 3.//忘记密码
   与注册账号类似
'''
def password_forget(request):
    if request.method == 'POST':
        #   get username and password from POST request
        post = json.loads(request.body)
        username = post['username']
        pwd = post['password']

        #   judge phone number or e-mail address, then check the validity of username
        if "@" in username:
            at_existed = True
            pattern = re.compile(r"^[-_\w\.]{0,64}@([-\w]{1,63}\.)*[-\w]{1,63}$")
        else:
            at_existed = False
            pattern = re.compile(r"^\d{11}$")
        if re.match(pattern, username) is None:
            return HttpResponse(json.dumps({
                                   'code':account_code['username_invalid'],
                                   'sessionKey': ''
                                }),content_type="text/plain")
        #   check the validity of password
        if not 6 <= len(pwd) <= 64:
            return HttpResponse(json.dumps({
                                   'code':account_code['password_invalid'],
                                   'sessionKey': ''
                                }),content_type="text/plain")

        #   check up whether the account has existed
        if at_existed:
            new_user = User.objects.filter(email=username)
        else:
            new_user = User.objects.filter(phone=username)
        if not new_user:
            return HttpResponse(json.dumps({
                                   'code':account_code['username_not_exist'],
                                   'sessionKey': ''
                                }),content_type="text/plain")
        else:
            #   update the password
            new_user.update(password=pwd)

        return HttpResponse(json.dumps({
                                   'code':account_code['reset_password_success'],
                                   'sessionKey': ''
                                }),content_type="text/plain")
    #   not a POST request
    elif request.method == 'OPTIONS':
        response = HttpResponse(json.dumps({
                                   'code':account_code['options_request'],
                                   'sessionKey': ''
                                }),content_type="text/plain")
        response['Access-Control-Allow-Origin'] = "*"
        return response
    else:
        return HttpResponse(json.dumps({
                                   'code':account_code['not_POST'],
                                   'sessionKey': ''
                                }),content_type="text/plain")



'''
  4.登出功能
  移除用户的Cookies
'''
def logout(request):
    if request.method == 'POST':
        sessionKey = request.META.get('HTTP_SESSIONKEY', None)
        if(sessionKey):
            s = SessionStore(session_key=sessionKey)
            del s['username']
            return HttpResponse(json.dumps({
                                   'code':account_code['logout_success'],
                                   'sessionKey': ''
                                }),content_type="text/plain")
        else:
            return HttpResponse(json.dumps({
                                   'code':account_code['logout_error'],
                                   'sessionKey': ''
                                }),content_type="text/plain")
    elif request.method == 'OPTIONS':
        response = HttpResponse(json.dumps({
                                   'code':account_code['options_request'],
                                   'sessionKey': ''
                                }),content_type="text/plain")
        response['Access-Control-Allow-Origin'] = "*"
        return response
    else:
        return HttpResponse(json.dumps({
                                   'code':account_code['not_POST'],
                                   'sessionKey': ''
                                }),content_type="text/plain")


def editProfile(request, id_user):
    if request.method == 'POST':
        post = json.loads(request.body)
        s = SessionStore(session_key=post['sessionKey'])
        if(s.get('username', False)):
            if "@" in s['username']:
                user = User.objects.get(email=s['username'])
            else:
                user = User.objects.get(phone=s['username'])
            if post['name'] == 'sex':
                user.sex = post['value']
            elif post['name'] == 'introduction':
                user.introduction = post['value']
            elif post['name'] == 'resident':
                user.resident = post['value']
            user.save()
            return HttpResponse('OK', content_type="text/plain")
        else:
            return HttpResponse("OJ8K", content_type="text/plain")
    else:
        return HttpResponse("OJ8K", content_type="text/plain")


def getProfile(request, id_user):
    if request.method == 'POST':
        s = SessionStore(session_key=request.body)
        if(s.get('username', False)):
            if "@" in s['username']:
                user = User.objects.get(email=s['username'])
            else:
                user = User.objects.get(phone=s['username'])
            info = {
                'sex': user.sex,
                'resident': user.resident,
                'introduction': user.introduction
            }
            return HttpResponse(json.dumps(info), content_type="text/plain")
        else:
            return HttpResponse("OJ8K", content_type="text/plain")
    else:
        return HttpResponse("OJ8K", content_type="text/plain")

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
