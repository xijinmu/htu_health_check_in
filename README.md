# 移动学工 自动健康签到脚本

> 声明：本程序完全开源免费，仅用于学习和交流使用，请勿用于非法用途，否则后果自负。
>
> 如果您使用本程序，即视为您同意上述条款。

Table of Contents
=================

* [移动学工 自动健康签到脚本](#移动学工-自动健康签到脚本)
   * [介绍](#介绍)
   * [环境要求](#环境要求)
   * [使用指南](#使用指南)
      * [用户信息 UserInfo](#用户信息-userinfo)
      * [邮箱配置 Mail](#邮箱配置-mail)
      * [百度智云ORC key](#百度智云orc-key)
      * [签到信息](#签到信息)
      * [日志和开启Cookies存储](#日志和开启cookies存储)
   * [部署](#部署)
      * [自己的服务器](#自己的服务器)
         * [修改配置文件](#修改配置文件)
         * [添加定时任务](#添加定时任务)
      * [使用云函数](#使用云函数)
         * [修改配置文件](#修改配置文件-1)
         * [新建函数服务](#新建函数服务)
         * [测试](#测试)
   * [几个要点](#几个要点)

## 介绍

本程序可以实现河南师范大学移动学工平台的每日健康打卡功能。主要有以下特点：

1. 配置简单：所有的配置都位于`/config/config.txt`配置文件中，多快好省。
2. 邮箱推送：实现的打卡信息的邮箱推送，以知道自己是否打卡成功。（失败则不会发送）
3. 支持云函数部署：无需服务器，省时省力省金钱。

## 环境要求

本程序由python编写，需要以下环境：

1. Python 3版本
2. 以下python包：
   1. `requests`
   2. `PyEmail`
   3. `beautifulsoup4`
   4. `configparser`

统一安装，使用`requirements.txt`文件在项目根目录中，执行下面的命令即可安装所需的所有包。

~~~bash
pip install -r requirements.txt
~~~

## 使用指南

本程序用户只需修改位于`/config/config.txt`的配置文件即可，然后使用Python解释运行根目录下的`/run.py`，如图所示：

![1](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715135219.png)

下面将进行详细讲解如何获取和填写。

> 注意：这里等号后面的值都无需加引号

### 用户信息 UserInfo

![image-20210715135928868](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715135928.png)

这里填写你的学号和真实姓名。userid是学号，name是姓名。

### 邮箱配置 Mail

![image-20210715135951318](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715135951.png)

这里主要用于每日的打卡情况推送，可以关闭或开启。打卡信息会由第三方SMTP服务器发送到`receiver`所指定的邮箱中。这里以QQ邮箱为例，展示如何获取这些信息。QQ邮箱的smtp服务器是 `smtp.qq.com`，用户名就算你的账户名，口令需要进入QQ邮箱设置中获取。

进入`设置-账户`找到**POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务**，开启SMTP服务。然后点击生成授权码进行获取。

![2](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715135226.png)

![3](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715135230.png)

### 百度智云ORC key

![image-20210715140017294](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715140017.png)

由于登录使用了图形验证码进行验证，所以需要进行ORC识别实现自动登录功能。这里使用百度智云的ORC服务，认证用户每月有1000次的免费次数，对于30天打卡足够了。

在这里，我们需要获取`ApiKey`和`SecretKey`这两个键的值。

打开网址 https://cloud.baidu.com/doc/OCR/s/9k3h7xuv6 点击领取免费资源，如果未注册登录则先注册登录。

![4](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715135236.png)

然后全选，全部领取即可。跳转到资源列表，点击**应用列表**，点击**新建应用**，输入应用名称即可获得`API Key`和`Secret Key`。只要保证数字识别在勾选着就可以了。

>  注意：未实名用户只有200次/月，请进行个人中心进行的个人实名认证！

![5](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715135240.png)

![6](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715135247.png)

![7](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715135254.png)

### 签到信息

下面的就是签到打卡的信息了。按照注释的说明进行填写即可。在这里，0代表**是**，1代表**否**，其余的看注释即可。位置信息复制上一次打卡的定位信息。

### 日志，Cookies 等项目的存储控制

默认开启日志和Cookies登录，开启为`on`，关闭为`off`。可以根据需要配置。如果部署再自己的服务器中则建议开启，这样可以减少资源的消耗。但是如果部署在云函数中，由于程序没有写入权限，则需要将下列功能全部关闭`off`。具体后面的部署小节中会进行说明。

![image-20210715232321380](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715232321.png)

## 部署

### 自己的服务器

#### 修改配置文件

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
0 7 * * * * /bin/python3 /home/ubuntu/qiandao/run.py
~~~

后面修改为自己程序的路径！根据自己的实际情况进行修改。

具体语法，参考[Cron表达式语法详解](https://blog.csdn.net/lianjunzongsiling/article/details/82228655)

### 使用云函数

#### 修改配置文件

首先，你应该参考上面的使用指南，修改好配置文件！！测试无误后再进行，以免麻烦。

> 注意：请先仔细阅读**使用指南**，并**配置好配置文件**之后在进行下面的操作。

#### 新建函数服务

使用腾讯云函数https://cloud.tencent.com/product/scf 的免费资源进行部署。首先，注册和登录请自行操作，之后我将进行具体的演示。

在控制面板中新建自定义函数。

![image-20210715171018887](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715171018.png)

创建方式选择自定义创建，然后填写基本配置，函数名称随意，运行环境选择`Python3.6`。

![image-20210715171324625](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715171324.png)

克隆本仓库，并参考上文中的**使用指南**进行配置，并将下列配置全部改为`off`！！这很重要！！

![image-20210715172157112](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715172157.png)

之后上传该文件夹。在`执行方法`中填入`run.yunRun`。

![image-20210715172333021](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715172333.png)

创建自定义触发器，在触发周期中选择**自定义触发周期**，这里的`0 10 7 * * * *`代表每天的七点十分零秒执行一次，具体的`Cron`格式参考[这里的文章](https://cloud.tencent.com/document/product/583/9708#cron-.E8.A1.A8.E8.BE.BE.E5.BC.8F)。

![image-20210715172532508](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715172532.png)

最后，点击完成！然后跳转至函数配置页面。之后点击**编辑**，向下找到`环境配置-执行超时时间`将其设置为20秒。然后在下面点击保存。

![image-20210715172945548](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715172945.png)

![image-20210715173124825](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715173124.png)

#### 测试

测试执行效果。点击**函数代码**，下滑找到**测试**和**部署**，点击测试即可开始运行。

![image-20210715173302341](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715173302.png)

![image-20210715173436632](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715173436.png)

测试成功！显示返回的结果和日志。

![image-20210715173427491](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210715173427.png)

此时，此云函数将在触发器设置的时间点执行，进行打卡和推送。

## 几个要点

1. 这些资源都是利用免费额度内的资源，请不要随便扩散和传播自己的token和SecretKey，否则后果自负。
2. 请在本地测试好配置文件无误后在进行云函数的上传操作，以免更改麻烦。
3. 如果使用云函数，请必须按照说明进行更改配置文件`config.txt`最后的设置！！！如果在自己的服务器中，则建议开启，以减少资源消耗。
4. 配置文件中，0代表**是**，1代表**否**
5. 目前不能多人打卡
6. 地址信息从往日的打卡信息中复制（微信登录即可方便复制）