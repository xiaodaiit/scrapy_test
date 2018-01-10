import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib

import re

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")
# print(session.cookies)
# session.cookies='_zap=a8d4039c-ea44-4168-a640-6bca63430f72; d_c0="AJBAjW1HNwqPTloDehA6xV9QqC28cAjWbDE=|1468288403"; _za=93866b57-56d6-465e-b3a7-a05f987e53eb; _ga=GA1.2.1739770305.1473390665; q_c1=c9afad19909246deb723e7e468ecc9cc|1507512307000|1468288403000; q_c1=c9afad19909246deb723e7e468ecc9cc|1512954173000|1468288403000; r_cap_id="N2Q2OGM5ZDllNDVlNGZiMzgwZGFhZTAxZjc5ZjY0M2Y=|1512954173|073985dc2375b213c5b1a326b654ef485a181f71"; cap_id="NjYyZTM2OTE2YWViNDljZDk1ZGMyNWZmNWEzOGUyYWI=|1512954173|ca05f981e14816d58862a92f9a2cdb6f4531502f"; z_c0=Mi4xQWhGNUFnQUFBQUFBa0VDTmJVYzNDaGNBQUFCaEFsVk5ReWNiV3dCbzJ0VFhlU3lxZ2VDckNORHppNWlNRnJaV213|1512954179|de030212c5d85eda626e96f2baa6b7ed7a6e8f26; aliyungf_tc=AQAAAIiwfTehtgMAIkgadkEp2cnTI4mm; __utma=51854390.1739770305.1473390665.1513675034.1513733291.35; __utmc=51854390; __utmz=51854390.1513733291.35.32.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100--|2=registration_date=20160113=1^3=entry_date=20160113=1; _xsrf=7a1d22dc-100d-4c5f-8986-8a4c479f5221'
# exit()

try:
    session.cookies.load(ignore_dicard=True)
except:
    print("cookie加载失败")
agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"

header = {
    "HOST" : "www.zhihu.com",
    "Referer" : "https://www.zhihu.com",
    "User-Agent" : agent
}

def is_login():
    #通过个人中心页面返回状态码来判断是否为登录涨态
    inbox_url = "https://www.zhihu.com/question"
    response = session.get(inbox_url, headers=header, allow_redirects=False)
    if response.status_code != 200:
        return False
    else:
        return True

def get_xsrf():
    #获取xsrf code
    response = session.get("https://www.zhihu.com", headers=header)
    res = response.text.replace("\n","")
    #注意去除换行符
    match_obj = re.match('.*name="_xsrf" value="(.*?)"', res)
    if match_obj:
        return match_obj.group(1)
    else:
        return "1"

def get_index():
    response = session.get("https://www.zhihu.com", headers=header)
    with open("inde.html", 'wb') as f:
        f.write(response.text.encode("utf-8"))
    print("ok")

def get_captcha():
    import time
    #验证码
    t = str(int(time.time()*1000))
    captcha_url ='https://www.zhihu.com/captcha.gif?r={0}&type=login'.format(t)
    t = session.get(captcha_url, headers = header)
    with open("captcha.jpg","wb") as f:
        f.write(t.content)
        f.close()
    from PIL import Image
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        pass
    captcha = input("验证码>\n")
    return captcha

def zhihu_login(account, password):
    #知乎登录
    if re.match("^1\d{10}",account):
        print("手机号码登录")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf" : get_xsrf(),
            'phone_num': account,
            'password': password,
            'captcha': get_captcha()
        }
    else:
        if "@" in account:
            post_url = "https://www.zhihu.com/login/email"
            post_data = {
                "_xsrf": get_xsrf(),
                "email": account,
                "password": password
            }

    response_text = session.post(post_url, data=post_data, headers=header)
    session.cookies.save()


zhihu_login('15010925302','dft123')
get_index()
print( is_login() )
# print( get_xsrf() )
# print( get_captcha() )