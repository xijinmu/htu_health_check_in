#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

def sendMail(receiver, htmlMsg):
    sender = 'imchen@88.com'
    receivers = [receiver]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    # 第三方 SMTP 服务
    mail_host="smtp.88.com"  #设置服务器
    mail_user="imchen@88.com"    #用户名
    mail_pass="kskXMd9YgYuUCf3V"   #口令 

    mail_msg = htmlMsg
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = Header("失眠孤岛chens.life", 'utf-8')
    message['To'] =  Header("打卡", 'utf-8')

    subject = '你的健康打卡数据推送'
    message['Subject'] = Header(subject, 'utf-8')


    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        print ("邮件发送成功")
    except smtplib.SMTPException:
        print ("Error: 无法发送邮件")