import time
from datetime import datetime


class Date(object):
    def __init__(self):
        self.year = time.localtime(time.time()).tm_year  # 获取年份
        self.month = time.localtime(time.time()).tm_mon  # 获取月份
        self.day = time.localtime(time.time()).tm_mday  # 获取几号
        self.hour = time.localtime(time.time()).tm_hour  # 获取小时
        self.minute = time.localtime(time.time()).tm_min  # 获取分钟
        self.sec = time.localtime(time.time()).tm_sec  # 获取秒

    def getDate(self, timestamp=None):
        timestamp = int(timestamp)
        if not timestamp:
            timestamp = time.time()
        self.year = time.localtime(timestamp).tm_year  # 获取年份
        self.month = time.localtime(timestamp).tm_mon  # 获取月份
        self.day = time.localtime(timestamp).tm_mday  # 获取几号
        self.hour = time.localtime(timestamp).tm_hour  # 获取小时
        self.minute = time.localtime(timestamp).tm_min  # 获取分钟
        self.sec = time.localtime(timestamp).tm_sec  # 获取秒
        return self.year, self.month, self.day, self.hour, self.minute, self.sec

    def getTimestamp(self, year=None, month=None, day=None, hour=None, minute=None, sec=None):
        if not year:
            year = datetime.now().year
        if not month:
            month = datetime.now().month
        if not day:
            day = datetime.now().day
        if not hour:
            hour = datetime.now().hour
        if not minute:
            minute = datetime.now().minute
        if not sec:
            sec = datetime.now().second
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.sec = sec
        date = f'{self.year}-{self.month}-{self.day} {self.hour}:{self.minute}:{self.sec}'
        fmt = '%Y-%m-%d %H:%M:%S'
        timestamp_list = time.strptime(date, fmt)
        timestamp = int(time.mktime(timestamp_list))
        return timestamp



if __name__ == '__main__':
    d = Date()
    # print(d.getTimestamp())
    # # print(d.getTimestamp())
    # time.sleep(3)
    # print(d.getTimestamp())
    # # print(d.getTimestamp())
    print(__name__)
    t = 1649516383
    print(d.getDate(t))
