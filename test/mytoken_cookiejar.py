


from http import cookiejar
from urllib import parse
from urllib import request
import re
from pprint import pprint
import time
from socket import timeout
from pprint import pprint


def fail_mytoken_CookieJar():
    # 创建一个Cookiejar的对象
    cookie = cookiejar.CookieJar()

    # 通过HTTPCookieProcessor处理cookie
    cookie_handler = request.HTTPCookieProcessor(cookie)

    # 构建一个opener
    #用一个新的cookie_handler去取代原来的默认http的处理
    opener = request.build_opener(cookie_handler)
    # 默认UA的设置类似
    opener.addheaders = [("User-Agent","Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36")]

    # 找到登录的入口
    urlLogin = "https://mytoken.io/api/user/login"
    #urlLogin = "http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp=2018402230928"

    # 登录的用户名和密码
    data = {
    'type':'1',
    'email':'missing64002@qq.com',
    'password':'ea21841da70e6405af19fabc4ff8bdd9',
    'remember':'true',
    'timestamp':str(int(time.time()*1000)),
    'code':'757e6b38a57184f28ff850b436102c39',
    'platform':'web_pc',
    'v':'1.0.0',
    'language':'zh_CN',
    'legal_currency':'CNY',
    }
    # 通过urlencode
    data = bytes(parse.urlencode(data),encoding="utf-8")
    # 发送一次post请求，生成登录成功之后的cookie
    req = request.Request(urlLogin, data=data,method="POST")
    response = opener.open(req) # 注意：这里使用的是opener去HTTP请求的

    # 获取到cookie之后，打开自己的个人主页
    responsemyRenren = opener.open("https://mytoken.io/")

    with open("myRenrenFromCookieJar.html","wb") as f:
        f.write(responsemyRenren.read())




headers = '''
accept:application/json, text/plain, */*
accept-encoding:gzip, deflate, br
accept-language:zh-CN
content-length:33
content-type:application/x-www-form-urlencoded
cookie:__cfduid=dbeda4c04bc0775798bd60dee365fcf191554636701; hotbit=3aab7dc747766b2f20f9e7212c407a46; __cfruid=cf902c3bc0c63b23d8f41fc64c78e812f8f22682-1559877945; lang=zh-CN; _ga=GA1.2.2032328484.1554636446; _gid=GA1.2.405442864.1559877790
dnt:1
origin:https://m.hotbit.io
referer:https://m.hotbit.io/
user-agent:Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1
'''

def get_headers_from_str(str_):
    lst = str_.split('\n')
    lst = [l.split(':',1) for l in lst if l.strip()]
    return lst

headers = get_headers_for_str(headers)
pprint(headers)