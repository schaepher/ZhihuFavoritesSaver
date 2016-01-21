# zhihuParser

用来提取知乎答案    
Python版本 3.5  
 
1. ZhihuParserWithGUI.py 可以运行在windows上，有GUI界面  
    输入地址的格式为：  
    http://www.zhihu.com/question/问题号  


2. ZhihuParser.py 没有界面，命令行的操作   
    一开始需要在login()里把账号密码填上：  
            login_data = {
             'email': 'xxx@xx.com',
             'password': 'xxxxx',
             'rememberme': 'true'
            }
            
    运行一次该文件，填入验证码即可登陆。  
    接着把底部的login()注释掉，把后两行的注释恢复，并在url里填写收藏夹地址
    再次运行该文件即可。
    
    * 现在的登陆很麻烦，接下去会对此进行优化
    * 有少数收藏没有解析到，上一个优化完后会解决该问题
    * 其他优化以后再说