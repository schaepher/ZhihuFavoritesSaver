# zhihuParser

用来提取知乎答案    
Python版本 3.5  
 
1. ZhihuParserWithGUI.py 可以运行在windows上，有GUI界面  
    输入地址的格式为：  
    http://www.zhihu.com/question/问题编号


2.  没有界面，命令行的操作
    * 一开始需要在config.ini里把账号密码填上（不用加引号）：
          [UserData]
          Email = xxxx@xxx.com
          Password = xxxx
      然后把收藏夹地址复制到[Collection]的url里（或者把“xxxxxx”换成收藏夹编号）：
          url = https://www.zhihu.com/collection/xxxxxx

    * 运行一次Login.py，填入验证码即可登陆。
      > 只需登录一次即可，以后要再用的时候，不必登录

    * 接着运行ZhihuParser.py即可


* 如果在一个问题下收藏了多个答案，只能获取第一个答案，接下去会解决该问题
* 其他优化以后再说