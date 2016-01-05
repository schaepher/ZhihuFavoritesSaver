def mkdir():
    import os
    path = ".\\result"
    is_exists = os.path.exists(path)
    if not is_exists:
        os.makedirs(path)
        os.chdir(path)
        return True
    else:
        os.chdir(path)
        return False


def write(title, data):
    out = open(title + '.html', 'w', encoding='utf-8')
    print(data, file=out)
    out.close()


def parser(url):
    import urllib.request
    from html.parser import HTMLParser
    import re

    html_bytes = urllib.request.urlopen().read()
    html = html_bytes.decode('UTF-8')

    title = re.compile(
            r'<h2 class="zm-item-title"><a target="_blank" href="/question/\d+">'
            r'(.+?)</a></h2>.+?<a class="author-link" data-tip=.+?>(.+?)</a>.+?'
            r'<div class="zm-item-vote-info " data-votecount="(\d+)">.+?'
            r'<textarea class="content hidden">(.+?)<span.+?</textarea>',
            re.DOTALL)
    content_array = title.findall(html)

    for i in range(len(content_array)):
        main_content = HTMLParser().unescape(content_array[i][3])
        main_content = re.sub('(<img.+?>)', '<br>\\1<br>', main_content)
        content = '<h2 align="center">' + content_array[i][0] + '</h2><br><span style="float:right;">赞数：' + \
                  content_array[i][2] + '</span><br><span style="float:right;">作者：' + content_array[i][
                      1] + '</span><br><br><div class="zm-editable-content clearfix">' + main_content + '</div>'

        write(str(i) + content_array[i][0], content)


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

    headers_base = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
        'Connection': 'keep-alive',
        'Host': 'www.zhihu.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
        'Referer': 'http://www.zhihu.com/'
    }
    url = 'http://www.zhihu.com/#signin'

        # cookie = http.cookiejar.CookieJar()
    cookie = http.cookiejar.MozillaCookieJar('cookie.ini')
    cookie_set = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(cookie_set)
    o = opener.open(url)
    html_bytes = o.read().decode('UTF-8')
    reg = r'name="_xsrf" value="(.*)"/>'
    pattern = re.compile(reg)
    result = pattern.findall(html_bytes)
    xsrf = result[0]
    login_data['_xsrf'] = xsrf

    captcha_url = 'http://www.zhihu.com/captcha.gif'
    captcha = urllib.request.Request(captcha_url, headers=headers_base)
    opener1 = urllib.request.build_opener(cookie_set)
    html_bytes = opener1.open(captcha)
    f = open('captcha.gif', 'wb')
    f.write(html_bytes.read())
    f.close()

    print('请输入验证码:')
    captcha_str = sys.stdin.readline()
    login_data['captcha'] = captcha_str[0:4]
    login_url = 'http://www.zhihu.com/login/email'
    login_data = urllib.parse.urlencode(login_data)
    login_data = login_data.encode('utf-8')
    start_login = urllib.request.Request(login_url, headers=headers_base)
    opener2 = urllib.request.build_opener(cookie_set)
    results1 = opener2.open(start_login, login_data)
    print(results1.read())
    cookie.save(ignore_discard=True, ignore_expires=True)

# mkdir()
# com()
login()
