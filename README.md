# ZhihuFavoritesSaver

用来将自己的收藏夹里的答案提取出来并保存为html文件    
Python版本 3.5    
 
###一、如果你没有安装python 3.5  

这里提供了可以直接在windows上使用的可执行文件。  
在“windows_version”这个文件夹里先配置config.ini再打开Main.exe，就可以使用了。  

---
 
###二、如果你有安装python 3.5  

那么有两种方式：第一种是只有命令行的操作（会比较常更新），第二种是图形化操作（基本没更新）。
 
1.  没有界面，命令行的操作
    * 一开始需要在config.ini里把账号密码填上（不用加引号）：   

      ```   
         [UserData]
         Email = xxxx@xxx.com
         Password = xxxx
      ```

    * 运行Main.py

    * 选择0，填入验证码即可登陆。
      > 只需登录一次即可，以后要再用的时候，不必登录

    * 选择1
      根据提示选择收藏夹所对应的序号，即可下载

    > 下一个把界面做上
    > 其他优化以后再说

2. ZhihuParserWithGUI.py 可以运行在windows上，有GUI界面  
    输入地址的格式为：  
    http://www.zhihu.com/question/问题编号


