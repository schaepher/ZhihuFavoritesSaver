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
    out = open(title + '.html', 'a', encoding='utf-8')
    print(data, file=out)
    out.close()


def parse(opener, url):
    import re
    import urllib.request
    import html

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

    questions = re.compile(r'zm-item-title">.+?<h2 class="', re.DOTALL)
    questions_array = questions.findall(html_content)
    questions_array_len = len(questions_array)

    title_re = re.compile(r'<a target="_blank" href="/question/\d+">(.+?)</a></h2>', re.DOTALL)

    answers = re.compile(
            r'.+?<div class="zm-item-vote-info " data-votecount="(\d+)">.+?data-author-name'
            r'="(.+?)" data-entry-url="(.+?)">.+?<textarea class="content hidden">(.+?)</textarea>',
            re.DOTALL)

    for index in range(questions_array_len):
        title_array = title_re.findall(questions_array[index])
        title_content = title_array[0]
        answers_array = answers.findall(questions_array[index])
        content_array_len = len(answers_array)
        for i in range(content_array_len):
            main_content = html.unescape(answers_array[i][3])
            main_content = re.sub('(<img.+?>)', '<br>\\1<br>', main_content)
            content = '<h2 align="center">' + title_content + '</h2>' + \
                      '<div align="center"><a href="https://www.zhihu.com' + answers_array[i][2] + \
                      '">www.zhihu.com' + answers_array[i][2] + '</a></div>' + \
                      '<br><span style="float:right;">赞数：' + \
                      answers_array[i][0] + '</span><br><span style="float:right;">作者：' + answers_array[i][1] + \
                      '</span><br><br><div class="zm-editable-content clearfix">' + main_content + '</div><br><br>'
            # 英文的问号'?'会使写入失败
            title = title_content.replace('?', '？')
            title = title.replace('\w', '')
            write_to_file(title, content)

    next_page_re = re.compile('<a href="\?page=(\d*)">下一页</a>', re.DOTALL)
    next_page = next_page_re.findall(html_content)
    next_page_len = len(next_page)
    if next_page_len > 0:
        return next_page[0]
    else:
        return ''


def get_opener():
    import urllib.request
    import http.cookiejar
    # 读取cookie
    file_name = 'cookie.txt'
    cookie_file = http.cookiejar.MozillaCookieJar()
    cookie_file.load(file_name, ignore_discard=True, ignore_expires=True)
    cookie_processor = urllib.request.HTTPCookieProcessor(cookie_file)
    opener = urllib.request.build_opener(cookie_processor)
    return opener


def start():
    import configparser
    import os
    config = configparser.ConfigParser()
    config.read('config.ini')
    url_data = config['Collection']
    url = url_data['url'] + '?page=1'
    opener = get_opener()

    # 切换到一个专门存放结果的目录中
    mkdir()
    path = ".\\result"
    os.chdir(path)

    # 开始获取
    print(url)
    next_page = parse(opener, url)
    while next_page != '':
        url_index = url.rfind('page=')
        url = url[0:url_index + 5] + next_page
        print(url)
        next_page = parse(opener, url)


start()
