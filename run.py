# -*- coding:UTF-8 -*-
import sign

# 云函数调用接口
def yunRun(event, context):
    try:
        sign.sign()
    except Exception as e:
        print(e)
        return("失败！")
    else:
        return("成功！")


if __name__=='__main__':
    sign.sign()