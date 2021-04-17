import time


def StrtoStamp(st):
    timeArray = time.strptime(st, "%Y-%m-%d %H:%M")
    # 转换为时间戳
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


def StamptoStr(tm):
    timeStamp = tm
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M", timeArray)
    # print(otherStyleTime)
    return otherStyleTime
