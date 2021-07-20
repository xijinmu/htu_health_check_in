import time
import datetime

# 获取北京时区时间Str
def getBeijingTimeStr():
    # 当前标准UTC时间
    utcNow = datetime.datetime.utcnow()
    # 当地偏移量
    # offset = int(time.localtime().tm_gmtoff/60/60)
    # 北京时间偏移量
    offset = 8
    # 使其偏移，格式化
    timeStr = (utcNow+datetime.timedelta(hours=offset)).strftime("%Y-%m-%d %H:%M:%S")
    return timeStr

# 返回未格式化的北京时间
def getBeijingTime():
    # 当前标准UTC时间
    utcNow = datetime.datetime.utcnow()
    # 当地偏移量
    # offset = int(time.localtime().tm_gmtoff/60/60)
    # 北京时间偏移量
    offset = 8
    # 使其偏移
    timeNow = utcNow+datetime.timedelta(hours=offset)
    return timeNow


if __name__=='__main__':
    print(getBeijingTime().strftime("%Y-%m-%d"))
    print(getBeijingTimeStr())