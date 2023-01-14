import random
import time
from datetime import datetime

def str_time_prop(start, end, time_format, prop):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))
def random_date():
  str_time =  str_time_prop("1/1/2018 1:30 PM", "10/10/2021 4:50 AM", '%m/%d/%Y %I:%M %p', random.random())
  datetime_datetime = datetime.strptime(str_time, '%m/%d/%Y %I:%M %p')
  return datetime.date(datetime_datetime)