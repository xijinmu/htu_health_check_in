# 移动学工 自动健康签到脚本

> 声明：本程序完全开源免费，仅用于学习和交流使用，请勿用于非法用途，否则后果自负。
>
> 如果您使用本程序，即视为您同意上述条款。

## 介绍

本程序可以自动的健康打卡，将其部署在服务器中即可

## 环境要求

本程序由python编写，需要以下环境：

1. Python 3版本
2. 以下python包：
   1. `requests`
   2. `PyEmail`
   3. `beautifulsoup4`
   4. `configparser`

直接使用命令统一安装包，`requirements.txt`在项目根目录。

~~~bash
pip install -r requirements.txt
~~~

## 使用指南

本程序用户只需修改位于`/config/config.txt`是配置文件即可，然后使用Python解释运行根目录下的`/run.py`，如图所示：

![1](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715135219.png)

下面将进行详细讲解如何获取和填写。

> 注意：这里等号后面的值都无需加引号

### 用户信息 UserInfo

这里填写你的学号和真实姓名。userid是学号，name是姓名。

### 邮箱配置 Mail

这里主要用于每日的打卡情况推送，可以关闭或开启。打卡信息会由第三方SMTP服务器发送到`receiver`所指定的邮箱中。这里以QQ邮箱为例，展示如何获取这些信息。QQ邮箱的smtp服务器是 `smtp.qq.com`，用户名就算你的账户名，口令需要进入QQ邮箱设置中获取。

进入`设置-账户`找到**POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务**，开启SMTP服务。然后点击生成授权码进行获取。

![2](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715135226.png)

![3](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715135230.png)

### 百度智云ORC key

由于登录使用了图形验证码进行验证，所以需要进行ORC识别实现自动登录功能。这里使用百度智云的ORC服务，认证用户每月有1000次的免费次数，对于30天打卡足够了。

在这里，我们需要获取`ApiKey`和`SecretKey`这两个键的值。

打开网址 https://cloud.baidu.com/doc/OCR/s/9k3h7xuv6 点击领取免费资源，如果未注册登录则先注册登录。

![4](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715135236.png)

然后全选，全部领取即可。跳转到资源列表，点击**应用列表**，点击**新建应用**，输入应用名称即可获得`API Key`和`Secret Key`。只要保证数字识别在勾选着就可以了。

![5](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715135240.png)

![6](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715135247.png)

![7](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715135254.png)

### 签到信息

下面的就是签到打卡的信息了。按照注释的说明进行填写即可。在这里，0代表**是**，1代表**否**，其余的看注释即可。位置信息复制上一次打卡的定位信息。

### 日志和开启Cookies存储

配置文件的下面可以开启日志和Cookies登录，开启为`on`，关闭为`off`。可以根据需要配置。在一些云函数机器中可能没有写入权限，这是则可以关闭这些功能。

## 部署

### 自己服务器

1. 首先确保满足了上述环境要求，接着克隆本仓库。
2. 进入文件夹中，修改`./config/config.txt`文件中的各项配置，看注释，根据自己前一天的信息填写。
3. 在根目录中解释执行`python ./run.py`

#### 添加定时任务

使用`crontab`定时任务。

~~~bash
crontab -e
~~~

在最末尾添加：

~~~bash
0 7 * * * /bin/python3 /home/ubuntu/qiandao/run.py
~~~

它的意思是在每天的七点整执行后面的命令，具体命令和路径参考自己的主机配置。

![image-20210715021934438](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715021934.png)

### 使用云函数

未测试

## 几个要点

1. 配置文件中，0代表**是**，1代表**否**
2. 目前不能多人打卡
3. 地址信息从往日的打卡信息中复制（微信登录即可方便复制）