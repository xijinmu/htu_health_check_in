# -*- coding:UTF-8 -*-
import configparser
import json
import requests
import base64
import getBeijingTime

def saveImg(img):
    with open('./img.png', 'wb') as f:
        f.write(img)
    return img

def getAccessToken(ApiKey, SecretKey):
    config = configparser.RawConfigParser()
    config.read("./config/config.txt", encoding="UTF-8")
    # 获取日期
    localtime = getBeijingTime.getBeijingTime().strftime("%Y-%m-%d")
    # 如果token已经存在,则直接读取,否则重新获取写入
    try:
        # 如果开启saveToken，则读取
        if config["token"]["saveToken"] == 'on':
            with open("./token/access_token.text", "r", encoding="UTF-8") as f:
                access_dict = json.loads(f.read().replace("'", '"'))
                # 如果日期登录今天，则直接使用，否则抛出异常重新获取
                if access_dict["time"] == localtime:
                    return access_dict["access_token"]
                else:
                    raise FileNotFoundError
        else:
            raise FileNotFoundError
    except:
        print("调用API获取token")
        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={ApiKey}&client_secret={SecretKey}'
        response = requests.get(host)
        if response:
            # 如果开启token存储
            if config["token"]["saveToken"] == 'on':
                with open("./token/access_token.text", "w", encoding="UTF-8") as f:
                    access_token = response.json()["access_token"]
                    access_dict = {
                        "time":localtime,
                        "access_token": access_token
                    }
                    f.write(str(access_dict))
            # 否则直接返回
            return response.json()["access_token"]
        else:
            print("Error in getAccessToken of orc.py!")

def orcNumber(ApiKey, SecretKey, img):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/numbers"
    # request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    # 二进制方式打开图片文件
    img = base64.b64encode(img)

    params = {"image":img}
    # 获取acess_token
    access_token = getAccessToken(ApiKey, SecretKey)
    # print(f'access_token={access_token}')
    if access_token == None:
        print("为设置ORC，请参照文档于配置文件中设置！")
        exit(1)
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        return response.json()
    else:
        print("Error in orcNumbner of orc.py!")

# 日志写入函数
def wirteLog(words_result):
    # 获取当前本地时间
    localtime = getBeijingTime.getBeijingTimeStr()
    with open('./log/orcLog.txt', 'a+') as f:
        f.writelines(localtime +' ' + words_result+'\n')

def getVerCode(url):
    config = configparser.RawConfigParser()
    config.read("./config/config.txt", encoding="UTF-8")
    ApiKey = config["ORC"]["ApiKey"]
    SecretKey = config["ORC"]["SecretKey"]
    success = False
    while success == False:
        # 传入URL，获取图片和Cookies
        imgRes = requests.get(url)
        img = imgRes.content
        if config["VerImg"]["saveImg"] == 'on':
            # 保存图片
            saveImg(img)
        orcRes = orcNumber(ApiKey, SecretKey, img)
        # orcRes = 2342
        # 写日志
        if config["Log"]["orcLog"] == 'on':
            wirteLog(str(orcRes))
        try:
            verCode = orcRes["words_result"][0]["words"]
            # return imgRes
            return verCode, imgRes
        except:
            print("Error: getVerCode in orc.py")
            continue

if __name__ == '__main__':
    verCode, imgRes = getVerCode("http://login.banjimofang.com/captcha/default?EloTEQ0Y")
    print(verCode)