# Python 3.5
def mkdir():
    import os
    path = ".\\result"
    is_exists = os.path.exists(path)
    if not is_exists:
        os.makedirs(path)
        return True
    else:
        return False


def write_to_file(title, data):
    out = open(title + '.html', 'w', encoding='utf-8')
    print(data, file=out)
    out.close()


def parse(url):
    import re
    import urllib.request
    import html
    import http.cookiejar
    import os
    # 读取cookie
    file_name = 'cookie.txt'
    cookie_file = http.cookiejar.MozillaCookieJar()
    cookie_file.load(file_name, ignore_discard=True, ignore_expires=True)
    cookie_processor = urllib.request.HTTPCookieProcessor(cookie_file)
    opener = urllib.request.build_opener(cookie_processor)

    headers_base = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
        'Connection': 'keep-alive',
        'Host': 'www.zhihu.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
        'Referer': 'http://www.zhihu.com/'
    }
    request_url = urllib.request.Request(url, headers=headers_base)
    result = opener.open(request_url)
    html_content = result.read().decode('UTF-8')

    # 切换到一个专门存放结果的目录中
    mkdir()
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
        main_content = html.unescape(content_array[i][3])
        main_content = re.sub('(<img.+?>)', '<br>\\1<br>', main_content)
        content = '<h2 align="center">' + content_array[i][0] + '</h2><br><span style="float:right;">赞数：' + \
                  content_array[i][2] + '</span><br><span style="float:right;">作者：' + content_array[i][
                      1] + '</span><br><br><div class="zm-editable-content clearfix">' + main_content + '</div>'
        title = content_array[i][0]
        # 英文的问号'?'会使写入失败
        title = title.replace('?', '？')
        title = title.replace('\w', '')
        write_to_file(title, content)


def start():
    import configparser
    config = configparser.ConfigParser()
    config.read('config.ini')
    url_data = config['Collection']
    url = url_data['url']
    parse(url)


start()
