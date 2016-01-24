# zhihuParser

用来提取知乎答案    
Python版本 3.5  
 
有两种方式：第一种是只有命令行的操作（会比较常更新），第二种是图形化操作（基本没更新）。
 
1.  没有界面，命令行的操作
    * 一开始需要在config.ini里把账号密码填上（不用加引号）：   

      ```   
         [UserData]
         Email = xxxx@xxx.com
         Password = xxxx
      ```
      
    * 运行一次Login.py，填入验证码即可登陆。
      > 只需登录一次即可，以后要再用的时候，不必登录

    * 接着运行ZhihuParser.py
      根据提示选择收藏夹所对应的序号，即可下载

    > 下一个把界面做上
    > 其他优化以后再说

2. ZhihuParserWithGUI.py 可以运行在windows上，有GUI界面  
    输入地址的格式为：  
    http://www.zhihu.com/question/问题编号


