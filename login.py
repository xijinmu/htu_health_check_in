# -*- coding:UTF-8 -*-
import json
import requests
import orc
import configparser
from bs4 import BeautifulSoup

# 构造登录数据
def makeInfo(userid, name, checkcode):
    head = {
        'User-Agent' :"Mozilla/5.0"
    }
    body = {
        'no': userid,
        'name': name,
        'checkcode': checkcode
    }
    return head, body

# 验证是否登录成功
def isLoginSuccess(response):
    if "验证码错误，请重试" in response.text:
        print("验证码错误，正在重试。。。")
        return "VerErr"
    elif "登陆失败！信息验证不通过（验证码正确，提交的信息不正确）" in response.text:
        print("登陆失败！信息验证不通过（验证码正确，提交的信息不正确）")
        return False
    elif "http://login.banjimofang.com/fields/login/student/6" == response.url:
        print("登录失效，重新登录！")
        return False
    else:
        return True

# 重新登录
def reLogin(config, session):
    while True:
        checkcode, imgRes = orc.getVerCode(config["System"]['verCodeApi'])
        head, body = makeInfo(config["UserInfo"]['userid'], config["UserInfo"]['name'], checkcode)
        session.get(config["System"]['loginGetApi'])
        # 登录
        response = session.post(config["System"]['loginPostApi'], headers=head, data=body, cookies=imgRes.cookies)
        # print(response.text)
        # print(response.url)
        # 如果登录成功
        isSuccess = isLoginSuccess(response)
        if isSuccess == True:
            if config["Cookie"]["saveCookie"] == 'on':
                # 更新Cookies文件
                with open("./cookies/cookies.txt", "w") as f:
                    f.write(str(response.cookies.get_dict()).replace("'",'"'))
            # 返回课程主页的 response
            return response
        # 如果是验证码错误，则重试
        elif isSuccess == "VerErr":
            continue
        # 其他错误，则返回
        else:
            return False

# 使用Cookies进行登录
def loginUseCookie(config, session):
    # 尝试打开cookies文件，如果不存在则返回False
    try:
        f = open("./cookies/cookies.txt", "r", encoding="UTF-8")
    except:
        # 获取失败
        print("cookies文件不存在，正在重新登录！")
        return False
    # 如果没有异常
    else:
        cookies = json.loads(f.read())
        # 获取主页面
        indexRes = session.post(str(config["System"]['indexApi']),headers={"User-Agent":"Mozilla/5.0"}, cookies=cookies)
        # print(indexRes.text)
        # print(indexRes.url)
        if isLoginSuccess(indexRes) == True:
            # 返回response
            return indexRes
        else:
            return False

# 返回用户信息的字典
# 包括 data_post_url college name
def returnInfo(response):
    soup = BeautifulSoup(response.text, 'html.parser')

    url = soup.find_all('a')[6].attrs['href']
    
    # 打卡Post Url
    daka_url = "https://htu.banjimofang.com"+url

    # 学院和年纪
    college = soup.find_all('a')[1].text

    # 包含名字的字符串
    strIncName = soup.find_all("script")[0].string
    start = strIncName.find("uname")+7
    end = strIncName.find("'", start)
    # 截取名字字符串
    name = strIncName[start: end]

    userInfo = {
        "daka_post_url": daka_url,
        "college": college,
        "name": name
    }

    return userInfo
'''
登录成功则返回包含用户信息和健康签到的Post Api的Dict，否则返回 False
这些key分别是
    daka_post_url
    college
    name
'''
def Login():
    session = requests.session()
    # 读取配置文件
    config = configparser.RawConfigParser()
    config.read("./config/config.txt", encoding="UTF-8")
    # userConfig = config.getUserConfig()
    # systemConfig = config.getSystemConfig()
    # 如果开启Cookie
    if config["Cookie"]["saveCookie"] == 'on':
        # 首先使用cookies进行登录
        res = loginUseCookie(config, session)
        if res:
            print("Cookies登录成功！")
            return returnInfo(res)
        else:
            res = reLogin(config, session)
            if res:
                print("重新登录成功！cookies文件已更新！")
                return returnInfo(res)
            else:
                return False
    # 如果没开启Cookie
    else:
        res = reLogin(config, session)
        if res:
            print("登录登录成功！")
            return returnInfo(res)
        else:
            return False



if __name__=='__main__':
    Info = Login()
    print(Info)