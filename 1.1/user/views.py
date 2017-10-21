from django.shortcuts import render
from django.shortcuts import HttpResponse
from user.models import User
from user import CheckAccountLegal

#这里不对，是对应账号的即时的IdenCode
global IdenCode
IdenCode = CheckAccountLegal.PhoneSendPassword()

# To do list
#Test : Test.txt

'''
    处理函数
'''
def AccountVerify(request):
    if request.method == "POST":
        mode = request.POST.get("submit")
        if mode == "Login":
            return LoginVerify(request)
        elif mode == "Register":
            return RegisterVerify(request)
        elif mode == "PasswordForget":
            return PasswordForget(request)
        elif mode == "PasswordChange":
            return PasswordChange(request)
        elif mode == "管理端":
            user_list = User.objects.all()
            return render(request, "show_account.html", {"data": user_list})
            #return Httpresponseredict("show_account/")
        else:
            return render(request, "account.html", {"info": "Not message"})
    return render(request, "account.html", {"info": "Not message"})


'''
1.//注册账号
  账号重名检测[注意账号类别]
  数据有效性、规范检测
  异常捕获
  存入数据库中
  返回登录信息
'''

def RegisterVerify(request):
    account = request.POST.get("account", None)
    pos_at = account.find('@')
    if pos_at < 0:  # phone
        if CheckAccountLegal.IsPhoneLegal(account) == False or CheckAccountLegal.CheckPhoneExist(account) == False:
            return render(request, "account.html", {"info": AccountInputWrong()})
        else:
            if User.objects.filter(phone = account):
                return render(request, "account.html", {"info": AccountExist()})
    else:  # email
        if CheckAccountLegal.IsEmailLegal(account) == False or CheckAccountLegal.CheckEmailExist(account) == False:
            return render(request, "account.html", {"info": AccountInputWrong()})
        elif User.objects.filter(email = account):
            return render(request, "account.html", {"info": AccountExist()})

    pwd = request.POST.get("password", None)
    if CheckAccountLegal.IsPasswordLegal(pwd) == False:
        return render(request, "account.html", {"info": PasswordIllegal()})
    else:
        if pos_at < 0:  # phone
            User.objects.create(phone=account, email=None, password=pwd)
        else:  # email
            User.objects.create(phone=None, email=account, password=pwd)
        return render(request, "account.html", {"info": AccountRegisterSucc()})


'''
2.//登陆
  账号存在检测[注意账号类别]
  密码匹配
  异常捕获
  返回登陆信息
'''

def LoginVerify(request):
    account = request.POST.get("account", None)
    pos_at = account.find('@')
    if pos_at < 0:  # phone
        if CheckAccountLegal.IsPhoneLegal(account) == False or CheckAccountLegal.CheckPhoneExist(account) == False:
            return render(request, "account.html", {"info": AccountInputWrong()})
        else:
            if User.objects.filter(phone = account):
                if User.objects.filter(phone=account, password=request.POST.get("password")):
                    return render(request, "account.html", {"info": AccountLoginSucc()})
                else:
                    return render(request, "account.html", {"info": AccountPasswordWrong()})
            else:
                return render(request, "account.html", {"info": AccountNonExist()})
    else:  # email
        if CheckAccountLegal.IsEmailLegal(account) == False or CheckAccountLegal.CheckEmailExist(account) == False:
            return render(request, "account.html", {"info": AccountInputWrong()})
        else:
            if User.objects.filter(email = account):
                if User.objects.filter(email=account, password=request.POST.get("password")):
                    return render(request, "account.html", {"info": AccountLoginSucc()})
                else:
                    return render(request, "account.html", {"info": AccountPasswordWrong()})
            else:
                return render(request, "account.html", {"info": AccountNonExist()})


'''
 3.//忘记密码
   与注册账号类似
'''

def PasswordForget(request):
    account = request.POST.get("account", None)
    pos_at = account.find('@')
    if pos_at < 0:  # phone
        if CheckAccountLegal.IsPhoneLegal(account) == False or CheckAccountLegal.CheckPhoneExist(account) == False:
            return render(request, "account.html", {"info": AccountInputWrong()})
        else:
            if User.objects.filter(phone = account):
                pass
            else:
                return render(request, "account.html", {"info": AccountNonExist()})
    else:  # email
        if CheckAccountLegal.IsEmailLegal(account) == False or CheckAccountLegal.CheckEmailExist(account) == False:
            return render(request, "account.html", {"info": AccountInputWrong()})
        else:
            if User.objects.filter(email = account):
                pass
            else:
                return render(request, "account.html", {"info": AccountNonExist()})

    if AccountVerifyUser() == True:  # 验证信息
        pos_at = account.find('@')
        # 生成验证码
        if pos_at < 0:  # phone
            IdenCode = CheckAccountLegal.PhoneSendPassword()
        else:  # email
            IdenCode = CheckAccountLegal.EmailSendPassword()
        return render(request, "account.html", {"info": AccountVerifyUserSucc()})
    else:
        return render(request, "account.html", {"info": AccountVerifyUserFail()})


def PasswordChange(request):
    account = request.POST.get("account", None)
    pos_at = account.find('@')
    if pos_at < 0:  # phone
        if CheckAccountLegal.IsPhoneLegal(account) == False or CheckAccountLegal.CheckPhoneExist(account) == False:
            return render(request, "account.html", {"info": AccountInputWrong()})
        else:
            if User.objects.filter(phone = account):
                pass
            else:
                return render(request, "account.html", {"info": AccountNonExist()})
    else:  # email
        if CheckAccountLegal.IsEmailLegal(account) == False or CheckAccountLegal.CheckEmailExist(account) == False:
            return render(request, "account.html", {"info": AccountInputWrong()})
        else:
            if User.objects.filter(email = account):
                pass
            else:
                return render(request, "account.html", {"info": AccountNonExist()})

    idencode = request.POST.get("idencode", None)
    if IdenCode == idencode:    # if 验证信息匹配，才能修改
        pwd = request.POST.get("password", None)
        if CheckAccountLegal.IsPasswordLegal(pwd) == False:
            return render(request, "account.html", {"info": PasswordIllegal()})
        else:
            if pos_at < 0:  # phone
                deldata = User.objects.filter(phone=account)
                deldata.delete()
                User.objects.create(phone=account, email=None, password=pwd)
            else:  # email
                deldata = User.objects.filter(email=account)
                deldata.delete()
                User.objects.create(phone=None, email=account, password=pwd)
            return render(request, "account.html", {"info": PasswordChangeSucc()})
    else:
        return render(request, "account.html", {"info": VerificationCodeWrong()})


'''
 4.//与前端vue.js 的表单功能结合
   探讨如何将网页表单数据传送到后端
   Django中的视图中，方法接收到的request对象有什么成员属性?如何利用?
   (使用vue.js的form 还是 Django的form 或者是其它解决方案?)
'''



def ShowAccount(request):
    user_list=User.objects.all()
    print("user_list="+user_list)
    return render(request,"show_account.html",{"data":user_list})



def AccountInputWrong():
    return "Wrong Account!"


def AccountNonExist():
    return "Account does not exist"


def AccountPasswordWrong():
    return "Wrong Password"


def AccountLoginSucc():
    return "Login successfully"


def AccountExist():
    return "Account has already existed"


def PasswordIllegal():
    return "Illegal password"


def AccountRegisterSucc():
    return "Register successfully"


def AccountVerifyUser():
    return True


def AccountVerifyUserSucc():
    return "Password has been sent to your device"


def AccountVerifyUserFail():
    return "Fail to verify user"

def PasswordChangeSucc():
    return "Change password successfully"

def VerificationCodeWrong():
    return "Wrong VerificationCode"

# elif "select * from models.User indexed by phone where phone == account" == None:
