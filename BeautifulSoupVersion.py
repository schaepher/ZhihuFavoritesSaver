# Python 3.5
import os
import urllib.request
import http.cookiejar
import re
import html

import sys
from bs4 import BeautifulSoup


class Parser:
    def __init__(self):
        self.__headers_base = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
            'Connection': 'keep-alive',
            'Host': 'www.zhihu.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
            'Referer': 'http://www.zhihu.com/'
        }

        self.__main_page = 'https://www.zhihu.com'

    @staticmethod
    def get_opener():
        # 读取cookie
        file_name = 'cookie.txt'
        cookie_file = http.cookiejar.MozillaCookieJar()
        cookie_file.load(file_name, ignore_discard=True, ignore_expires=True)
        cookie_processor = urllib.request.HTTPCookieProcessor(cookie_file)
        opener = urllib.request.build_opener(cookie_processor)
        return opener

    def get_collection_list(self, opener, url):
        if 'collections' not in url:
            index = url.find('people')
            user_name = url[index + 7:]
            url = 'https://www.zhihu.com/people/{}/collections'.format(user_name)

        request_collection = urllib.request.Request(url, headers=self.__headers_base)
        result = opener.open(request_collection)
        html_content = result.read().decode('UTF-8')
        soup = BeautifulSoup(html_content, 'html.parser')
        collections = soup.find_all('div', 'zm-item')
        # 如果不是‘www.zhihu.com/collections/号码’这种页面，尝试‘www.zhihu.com/people/用户名/collections’这种页面
        if len(collections) == 0:
            collections = soup.find_all('div', 'zm-profile-fav-item-title-wrap')

        print('收藏夹列表：')
        index = 0
        for collection in collections:
            title = collection.a.get_text()
            num = collection.find('span', href='javavscript:;').get_text()
            print(str(index) + ': ' + title + ' (' + num + ')')
            index += 1

        print('\n请选择序号(输入exit退出)：')
        num_selected = sys.stdin.readline()
        is_digit = re.match(r'\d+', num_selected)
        if is_digit:
            collection = collections[int(num_selected)]
            col_url = 'https://www.zhihu.com' + collection.a['href'] + '?page=1'
            # 切换到一个专门存放结果的目录中，以收藏夹的名字命名
            path = '.\\' + collection.a.get_text()
            self.mkdir(path)
            os.chdir(path)
            return col_url
        else:
            return False

    def parse(self, opener, url):
        request_url = urllib.request.Request(url, headers=self.__headers_base)
        link = opener.open(request_url)
        html_content = link.read()
        html_content = html_content.decode('UTF-8')
        html_content = html.unescape(html_content)
        soup = BeautifulSoup(html_content, 'html.parser')
        next_page_num = soup.find('a', text='下一页')
        if next_page_num is not None:
            next_page_num = next_page_num['href']
            next_page_num = next_page_num.replace('?page=', '')
        else:
            next_page_num = False

        answers = soup.find_all('div', 'zm-item')
        file = BeautifulSoup('', 'html.parser')
        title = ''
        for answer in answers:
            if answer.h2 is not None:
                if title != '':
                    try:
                        self.__write(title, file)
                    except RecursionError as e:
                        print('写入文件时出现异常，文件名为：' + title)

                title = answer.h2.get_text()
                file.reset()
                file = BeautifulSoup('<!DOCTYPE html><meta charset="utf-8"/>', 'html.parser')
                title_tag = file.new_tag('h2', align='center')
                title_tag.string = title
                file.append(title_tag)
            else:
                black_line = file.new_tag('div', style='height:2px; background-color:#000000;')
                file.append(black_line)
            # 答案地址
            div_center = file.new_tag('div', align='center')
            answer_href = self.__main_page + answer.link['href']
            href_tag = file.new_tag('a', href=answer_href)
            href_tag.string = answer_href
            div_center.append(href_tag)
            file.append(div_center)
            br_tag = file.new_tag('br')
            file.append(br_tag)
            # 赞同数
            span_vote = file.new_tag('span', style='float:right')
            span_vote.string = '赞同数：' + answer.find('span', class_='count').get_text()
            file.append(span_vote)
            br_tag = file.new_tag('br')
            file.append(br_tag)
            # 答主
            author_name = answer.find('div', class_='zm-item-rich-text')
            if author_name is not None:
                author_name = author_name['data-author-name']
            else:
                # 回答被建议修改
                title = None
                continue
            span_writer = file.new_tag('span', style='float:right')
            span_writer.string = "答主：" + author_name
            file.append(span_writer)
            br_tag = file.new_tag('br')
            file.append(br_tag)
            br_tag = file.new_tag('br')
            file.append(br_tag)
            # 内容
            text_area = answer.textarea
            text_area.name = 'div'
            del text_area['hidden']
            del text_area['class']
            file.append(text_area)
            br_tag = file.new_tag('br')
            file.append(br_tag)
            # 最后修改日期
            time = answer.find('a', class_='answer-date-link meta-item')
            edit_time = file.new_tag('div')
            edit_time.string = time.get_text()
            file.append(edit_time)
        return next_page_num

    def start(self):
        opener = self.get_opener()
        collections_url = "https://www.zhihu.com/collections/mine"
        url = self.get_collection_list(opener, collections_url)
        while url is not False:
            # 开始获取
            print('开始获取....')
            print('第1页')
            next_page = self.parse(opener, url)
            while next_page is not False:
                url_index = url.rfind('page=')
                url = url[0:url_index + 5] + next_page
                print('第{}页'.format(next_page[6:]))
                next_page = self.parse(opener, url)
            print('获取完毕！\n\n')
            os.chdir('..')
            url = self.get_collection_list(opener, collections_url)

    @staticmethod
    def mkdir(path):
        is_exists = os.path.exists(path)
        if not is_exists:
            os.makedirs(path)
            return True
        else:
            return False

    @staticmethod
    def __write(title, data):
        title = str(title)
        title = title.replace('?', '？')
        title = title.replace('\\', '_')
        title = title.replace('/', '_')
        title = title.replace('*', '_')
        title = title.replace('|', '_')
        title = title.replace('<', '_')
        title = title.replace('>', '_')
        title = title.replace(':', '_')
        title = title.replace('"', '_')
        out = open(title + '.html', 'a', encoding='utf-8')
        print(data, file=out)
        out.close()


soupS = Parser()
soupS.start()
