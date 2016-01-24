def main():
    import Login
    import ZhihuParser
    import sys
    print('0:登陆\t1:下载\t3:退出')
    line = sys.stdin.readline()
    line = line.replace('\n', '')
    while line != '3':
        if line == '0':
            Login.login()
        elif line == '1':
            ZhihuParser.start()
        else:
            print("输入错误，请重新输入")
        print('0:登陆\t1:下载\t3:退出')
        line = sys.stdin.readline()
        line = line.replace('\n', '')


main()
