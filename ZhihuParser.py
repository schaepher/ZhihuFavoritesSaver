headers_base = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
    'Connection': 'keep-alive',
    'Host': 'www.zhihu.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
    'Referer': 'http://www.zhihu.com/'
}


def mkdir():
    import os
    path = ".\\result"
    is_exists = os.path.exists(path)
    if not is_exists:
        os.makedirs(path)
        return True
    else:
        return False


def write(title, data):
    # 截取标题长度，否则太长会导致错误
    title = title[0:30]
    out = open(title + '.html', 'w', encoding='utf-8')
    print(data, file=out)
    out.close()


def parse(url):
    import re
    import urllib.request
    from html.parser import HTMLParser
    import http.cookiejar
    import os
    file_name = 'cookie.txt'
    cookie_file = http.cookiejar.MozillaCookieJar()
    cookie_file.load(file_name, ignore_discard=True, ignore_expires=True)
    cookie_processor = urllib.request.HTTPCookieProcessor(cookie_file)

    opener = urllib.request.build_opener(cookie_processor)

    html_content = urllib.request.Request(url, headers=headers_base)
    result = opener.open(html_content)
    html_content = result.read().decode('UTF-8')

    # 切换到一个专门存放结果的目录中
    path = ".\\result"
    os.chdir(path)

    title = re.compile(
            r'<h2 class="zm-item-title"><a target="_blank" href="/question/\d+">'
            r'(.+?)</a></h2>.+?<a class="author-link" data-tip=.+?>(.+?)</a>.+?'
            r'<div class="zm-item-vote-info " data-votecount="(\d+)">.+?'
            r'<textarea class="content hidden">(.+?)<span.+?</textarea>',
            re.DOTALL)
    content_array = title.findall(html_content)
    content_array_len = len(content_array)
    for i in range(content_array_len):
        main_content = HTMLParser().unescape(content_array[i][3])
        main_content = re.sub('(<img.+?>)', '<br>\\1<br>', main_content)
        content = '<h2 align="center">' + content_array[i][0] + '</h2><br><span style="float:right;">赞数：' + \
                  content_array[i][2] + '</span><br><span style="float:right;">作者：' + content_array[i][
                      1] + '</span><br><br><div class="zm-editable-content clearfix">' + main_content + '</div>'

        write(content_array[i][0], content)


def login():
    import sys
    import urllib.request
    import urllib.parse
    import re
    import http.cookiejar

    login_data = {
        'email': '',
        'password': '',
        'rememberme': 'true'
    }

    # 打开保存cookie的文件，并设置cookie
    cookie_file = http.cookiejar.MozillaCookieJar('cookie.txt')
    cookie_processor = urllib.request.HTTPCookieProcessor(cookie_file)
    opener = urllib.request.build_opener(cookie_processor)

    # 获取xsrf，登陆的验证需要这个
    url = 'http://www.zhihu.com/#signin'
    html_open = opener.open(url)
    html_content = html_open.read().decode('UTF-8')
    reg = r'name="_xsrf" value="(.*)"/>'
    pattern = re.compile(reg)
    result = pattern.findall(html_content)
    xsrf = result[0]
    login_data['_xsrf'] = xsrf

    # 获取验证码
    captcha_url = 'http://www.zhihu.com/captcha.gif'
    captcha = urllib.request.Request(captcha_url, headers=headers_base)
    html_content = opener.open(captcha)
    f = open('验证码.gif', 'wb')
    f.write(html_content.read())
    f.close()

    # 把验证码放入请求的头部
    print('请输入验证码（验证码图片在该程序所在的文件夹内）:\n')
    captcha_str = sys.stdin.readline()
    login_data['captcha'] = captcha_str[0:4]

    # 登陆。要对login_data进行编码上的处理，否则会出错
    login_url = 'http://www.zhihu.com/login/email'
    login_data = urllib.parse.urlencode(login_data)
    login_data = login_data.encode('utf-8')
    start_login = urllib.request.Request(login_url, headers=headers_base)
    result = opener.open(start_login, login_data)
    html_content = result.read().decode('UTF-8')
    print(html_content)
    # 将返回的字符串转为字典dic
    result = eval(html_content)
    result = result.get('msg')
    print(result)
    cookie_file.save(ignore_discard=True, ignore_expires=True)


mkdir()
login()
# m_url = 'https://www.zhihu.com/collection/???'
# parse(m_url)
