# Python 3.5
ANSWER_COUNT = 0
FAIL_COUNT = 0
FAIL_ARRAY = []

headers_base = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
    'Connection': 'keep-alive',
    'Host': 'www.zhihu.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
    'Referer': 'http://www.zhihu.com/'
}


def mkdir(path):
    import os
    is_exists = os.path.exists(path)
    if not is_exists:
        os.makedirs(path)
        return True
    else:
        return False


def write_to_file(title, data):
    # 替换掉在windows中不合法的文件名字符
    title = title.replace('?', '？')
    title = title.replace('\\', '_')
    title = title.replace('/', '_')
    title = title.replace('*', '_')
    title = title.replace('|', '_')
    title = title.replace('<', '_')
    title = title.replace('>', '_')
    title = title.replace(':', '_')
    title = title.replace('"', '_')
    out = open(title, 'a', encoding='utf-8')
    print(data, file=out)
    out.close()


def parse(opener, url):
    import re
    import urllib.request
    import html
    global ANSWER_COUNT
    global FAIL_ARRAY
    global FAIL_COUNT
    request_url = urllib.request.Request(url, headers=headers_base)
    result = opener.open(request_url)
    html_content = result.read()
    html_content = html_content.decode('UTF-8')
    questions = re.compile(r'zm-item-title">.+?<h2 class="', re.DOTALL)
    questions_array = questions.findall(html_content)
    questions_array_len = len(questions_array)

    title_re = re.compile(r'<a target="_blank" href="/question/\d+">(.+?)</a></h2>', re.DOTALL)

    answers_re = re.compile(
        r'.+?<div class=.+?data-votecount="(\d+)">.+?data-author-name'
        r'="(.+?)" data-entry-url="(.+?)">.+?<textarea hidden class="content">(.+?)</textarea>'
        r'.+?answer-date-link.+?>(.+?)</a>',
        re.DOTALL)

    for index in range(questions_array_len):
        title_array = title_re.findall(questions_array[index])
        title_content = title_array[0]
        answers_array = answers_re.findall(questions_array[index])
        content_array_len = len(answers_array)
        if content_array_len == 0:
            print('获取《{}》失败'.format(title_content))
            fail_link_re = re.compile(title_content + r'.+?<link itemprop="url" href="(.+?)">', re.DOTALL)
            link_array = fail_link_re.findall(questions_array[index])
            author_re = re.compile(title_content + r'.+?<a class="author-link".+?>(.+?)</a>', re.DOTALL)
            author_array = author_re.findall(questions_array[index])
            if len(author_array) == 1:
                author_name = author_array[0]
                print('答主为：{}'.format(author_name))
            elif len(author_array) > 1:
                author_name = '、'.join(author_array)
                print('可能为这些答主：{}'.format(author_name))
            else:
                author_name = '匿名答主'
                print(author_name)
            fail_link = '、'.join(link_array)
            FAIL_ARRAY.append(title_content + "答主：{}  链接：{}".format(author_name, fail_link))
            FAIL_COUNT += 1
            continue

        for i in range(content_array_len):
            main_content = html.unescape(answers_array[i][3])
            main_content = re.sub('(<img.+?>)', '<br>\\1<br>', main_content)
            main_content = re.sub(' width=\"\d+\" ', ' width="630" ', main_content)
            content = '<!DOCTYPE html>\n<meta charset="utf-8"/>\n<h2 align="center">' + title_content + '</h2>\n' + \
                      '<div align="center">\n<a href="https://www.zhihu.com' + answers_array[i][2] + \
                      '">www.zhihu.com' + answers_array[i][2] + '</a>\n</div>\n' + \
                      '<br>\n<span style="float:right;">赞数：' + \
                      answers_array[i][0] + '</span>\n<br>\n<span style="float:right;">作者：' + answers_array[i][1] + \
                      '</span>\n<br><br>\n<div class="zm-editable-content clearfix">' + main_content + '</div>\n' + \
                      '<br><br>' + answers_array[i][4] + '<br><br>'
            print('正在准备写入：' + title_content)
            write_to_file(title_content + '.html', content)
            ANSWER_COUNT += 1

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


def get_collection_list(opener):
    import urllib.request
    import re
    import sys
    import os
    url = "https://www.zhihu.com/collections/mine"
    request_collection = urllib.request.Request(url, headers=headers_base)
    result = opener.open(request_collection)
    html_content = result.read()
    html_content = html_content.decode('UTF-8')

    title_re = re.compile(r'<a href="/collection/(\d+)" >(.+?)</a>.+?<span href'
                          r'="javavscript:;">(.+?)</span>', re.DOTALL)
    title_array = title_re.findall(html_content)
    title_len = len(title_array)
    print('收藏夹列表：')
    for index in range(title_len):
        print(str(index) + '\t: ' + title_array[index][1] + '（' + title_array[index][2] + '）')
    print('\n请选择序号(输入exit退出)：')
    line = sys.stdin.readline()
    is_digit = re.match(r'\d+', line)
    if is_digit:
        line = int(line)
        if 0 <= line <= title_len - 1:
            question_number = title_array[line][0]
            url = url.replace('collections/mine', 'collection/' + question_number)
            url += '?page=1'

            # 切换到一个专门存放结果的目录中，以收藏夹的名字命名
            path = '.\\' + title_array[line][1]
            mkdir(path)
            os.chdir(path)
            return url
        else:
            return False
    else:
        return False


def start():
    import os
    opener = get_opener()
    global ANSWER_COUNT
    global FAIL_ARRAY
    global FAIL_COUNT
    # 获取收藏夹列表
    url = get_collection_list(opener)

    while url is not False:
        url = 'https://www.zhihu.com/collection/43031068?page=13'
        ANSWER_COUNT = 0
        FAIL_ARRAY = []
        FAIL_COUNT = 0
        # 开始获取
        print('开始获取....')
        print('第1页')
        next_page = parse(opener, url)
        while next_page != '':
            url_index = url.rfind('page=')
            url = url[0:url_index + 5] + next_page
            print('第' + str(next_page) + '页')
            next_page = parse(opener, url)
        print('获取完毕！\n共下载{}个答案'.format(ANSWER_COUNT))

        os.chdir('..')
        if FAIL_COUNT != 0:
            print('以下答案无法获取，可能是因为回答被建议修改：')
            for fail in FAIL_ARRAY:
                print(fail)
            write_to_file('fail_file.txt', '\n'.join(FAIL_ARRAY))
        print('\n\n')
        url = get_collection_list(opener)
