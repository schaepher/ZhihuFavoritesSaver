# Python 3.5
def login():
    import sys
    import urllib.request
    import urllib.parse
    import re
    import http.cookiejar
    import configparser
    from os import remove
    from os import system
    from os import getcwd
    import time
    login_data = {
        'email': '',
        'password': '',
        '_xsrf': '',
        'rememberme': 'true'
    }
    # 从配置文件读取账号密码
    config = configparser.ConfigParser()
    config.read('config.ini')
    user_data = config['UserData']
    login_data['email'] = user_data['Email']
    login_data['password'] = user_data['Password']

    headers_base = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
        'Connection': 'keep-alive',
        'Host': 'www.zhihu.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
        'Referer': 'http://www.zhihu.com/'
    }

    # 打开保存cookie的文件，并设置cookie
    cookie_file = http.cookiejar.MozillaCookieJar('cookie.txt')
    cookie_processor = urllib.request.HTTPCookieProcessor(cookie_file)
    opener = urllib.request.build_opener(cookie_processor)

    # 获取xsrf，登陆的验证需要xsrf
    request_signin = 'http://www.zhihu.com/#signin'
    html_open = opener.open(request_signin)
    html_content = html_open.read().decode('UTF-8')
    reg = r'name="_xsrf" value="(.*)"/>'
    pattern = re.compile(reg)
    result = pattern.findall(html_content)
    xsrf = result[0]
    login_data['_xsrf'] = xsrf

    # 获取验证码，并保存到本地
    code = str(int(1000 * time.time()))[0:13]
    captcha_url = 'https://www.zhihu.com/captcha.gif?r={}&type=login'.format(code)
    request_captcha = urllib.request.Request(captcha_url, headers=headers_base)
    html_content = opener.open(request_captcha)
    f = open('验证码.gif', 'wb')
    f.write(html_content.read())
    f.close()

    # 把验证码放入请求的头部
    print('正在打开验证码，请稍候....')
    path = getcwd() + '\\验证码.gif'
    system("START %s" % path)
    print('请输入验证码（验证码图片在该程序所在的文件夹内）:\n')
    captcha_str = sys.stdin.readline()
    login_data['captcha'] = captcha_str[0:4]

    # 登陆。要对login_data进行编码上的处理，否则会出错
    login_url = 'http://www.zhihu.com/login/email'
    login_data = urllib.parse.urlencode(login_data)
    login_data = login_data.encode('utf-8')
    request_login = urllib.request.Request(login_url, headers=headers_base)
    result = opener.open(request_login, login_data)
    html_content = result.read().decode('UTF-8')
    # print(html_content)
    # 将返回的字符串转为字典dic
    result = eval(html_content)
    result = result.get('msg')
    print(result)
    cookie_file.save(ignore_discard=True, ignore_expires=True)
    remove('验证码.gif')
