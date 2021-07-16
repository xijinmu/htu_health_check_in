# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

def sendMail(config, htmlMsg):
    sender = config["Mail"]["mail_user"]
    receivers = [config["Mail"]["receiver"]]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    # 第三方 SMTP 服务
    mail_host=config["Mail"]["mail_host"]  #设置服务器
    mail_user=config["Mail"]["mail_user"]    #用户名
    mail_pass=config["Mail"]["mail_pass"]   #口令 

    mail_msg = htmlMsg
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = Header(" 健康打卡推送", 'utf-8')
    message['To'] =  Header("打卡", 'utf-8')

    subject = '健康打卡数据推送'
    message['Subject'] = Header(subject, 'utf-8')


    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        print ("邮件发送成功")
    except smtplib.SMTPException as e:
        # 打印错误
        print(e)
        print ("Error: 无法发送邮件")