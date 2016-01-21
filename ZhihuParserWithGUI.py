def mkdir():
    import os
    path = ".\\result"
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        os.chdir(path)
        return True
    else:
        os.chdir(path)
        return False


def write(title, data):
    import os
    out = open(title + '.html', 'w', encoding='utf-8')
    print(data, file=out)
    out.close


def parser(url):
    import urllib.request
    import re

    htmlBytes = urllib.request.urlopen(url).read()
    html = htmlBytes.decode('UTF-8')

    title = re.compile(r'<h2.+?>\s+(.+?)\s+</h2>', re.DOTALL)
    titleArray = title.findall(html)

    voteNum = re.compile(r'<div class="zm-item-vote-info " data-votecount="(\d+)"', re.DOTALL)
    voteArray = voteNum.findall(html)

    name = re.compile(r'<a class="author-link" data-tip=".+?>(.+?)</a>', re.DOTALL)
    nameArray = name.findall(html)

    answer = re.compile(r'<div class="zm-editable-content clearfix">.+?</div>', re.DOTALL)
    answerArray = answer.findall(html)

    content = '<h2 align="center">' + titleArray[0] + '</h2><br><span style="float:right;">赞数：' + voteArray[
        0] + '</span><br><span style="float:right;">作者：' + nameArray[0] + '</span><br><br>' + answerArray[0]

    write(titleArray[0], content)


def main():
    url = entry.get()
    parser(url)


from tkinter import Tk, Label, Entry, Button, StringVar

rootView = Tk()
rootView.title("知乎答案提取器")
rootView.geometry('300x200')

label = Label(rootView, text="知乎问题页面的URL:", font=('Arial', 15))
label.pack()

var = StringVar()
entry = Entry(rootView, textvariable=var, bg="#CCCCCC")
entry.pack(after=label, fill="x")

btn_transfer = Button(rootView, text="转换", width=20, bg="#1C86EE", command=main)
btn_transfer.pack(side="bottom")

rootView.mainloop()
