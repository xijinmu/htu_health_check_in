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

## 使用方法

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