
from urllib import request

# 默认的头
HEADERS = {
'accept':'application/json, text/plain, */*',
'accept-language':'zh-CN',
'content-type':'application/json;charset=utf-8',
'cookie':'mytoken_sid=7c718a88b291842903892c69a1bf0153; Hm_lvt_42ea409f1dfb55e7603f23c9e1b7ebbf=1534822449,1534851996,1534852420,1534865623; Hm_lpvt_42ea409f1dfb55e7603f23c9e1b7ebbf=1534865623',
'dnt':'1',
'referer':'https://mytoken.io/',
'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36 Maxthon/5.1.3.2000',
'x-devtools-emulate-network-conditions-client-id':'18936b13-66f7-468e-a9f6-2c2fe730de55',
}


def request_get(url,headers=HEADERS):
    req = request.Request(url, headers=headers,)
    response = request.urlopen(req,timeout = 10)
    return response.read()







def mytoken_CookieJar():
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













def main():
    host = 'http://p1.xiaoshidi.net/'
    data = request_get('https://manhua.fzdm.com/39/117/index_3.html')

    data = data.decode('utf-8')

    import re
    data = re.findall(r'var mhurl="(.+?)"',data)

    url = host + data[0]
    print(url)
    data = request_get(url)

    filename = '1.jpg'
    with open(filename,'wb') as f:
        f.write(data)

if __name__ == '__main__':
    main()

