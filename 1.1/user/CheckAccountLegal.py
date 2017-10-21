
from user import models
import re


'''
*大陆号码或香港号码均可
'''
def IsPhoneLegal(str):
    #return IsChinaPhoneLegal(str) or IsHKPhoneLegal(str)
    return IsChinaPhoneLegal(str)

'''
*大陆手机号码11位数，匹配格式：前三位固定格式 + 后8位任意数
                           * 此方法中前三位格式有：
*13 + 任意数
      * 15 + 除4的任意数
             * 18 + 除1和4的任意数
                    * 17 + 除9的任意数
                           * 147
                           * /
'''
def IsChinaPhoneLegal(str):
    result = re.match(r"^((13[0-9])|(15[^4])|(18[0,2,3,5-9])|(17[0-8])|(147))\d{8}$", str)
    if result == None:
        return False
    else:
        return True

'''
*香港手机号码8位数，5 | 6 | 8 | 9
开头 + 7
位任意数
'''
def IsHKPhoneLegal(str):
    result = re.match(r"^(5|6|8|9)\d{7}$", str)
    if result == None:
        return False
    else:
        return True

def IsEmailLegal(str):
    result = re.match(r"^[-_\w\.]{0,64}@([-\w]{1,63}\.)*[-\w]{1,63}$", str)
    if result == None:
        return False
    else:
        return True

def CheckPhoneExist(str):
    return True

def CheckEmailExist(str):
    #check from some websits such as "https://verify-email.org/"
    return True

def IsPasswordLegal(str):
    return len(str)>=6 and len(str)<=64

def PhoneSendPassword():
    # http://blog.csdn.net/jinnian_lin/article/details/37876657
    return "123456"

def EmailSendPassword():
    #http: // blog.csdn.net / xiaosongbk / article / details / 60142996
    return "123456"

def UpdateAccount():
    phone = re.findall(r"^((13[0-9])|(15[^4])|(18[0,2,3,5-9])|(17[0-8])|(147))\d{8}$", models.User.phone)
    email = re.findall(r"^[-_\w\.]{0,64}@([-\w]{1,63}\.)*[-\w]{1,63}$", models.User.email)

