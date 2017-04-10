# -*- coding:utf-8 -*-
#该文件大部分提供的是基于日期的帮助方法 通过ct的ALL_CAL_FILE http://file.tushare.org/static/calAll.csv
import datetime  #时区
import time  #一天内的时间函数
import pandas as pd
from tushare.stock import cons as ct  #股票内常量文件

def year_qua(date):
    mon = date[5:7]   #mon是2015-05-07月度数据
    mon = int(mon)
    return[date[0:4], _quar(mon)]  #返回'2015',2 list数据
    

def _quar(mon):
    if mon in [1, 2, 3]:  #判断是第几季度
        return '1'
    elif mon in [4, 5, 6]:
        return '2'
    elif mon in [7, 8, 9]:
        return '3'
    elif mon in [10, 11, 12]:
        return '4'
    else:
        return None
 
 
def today():
    day = datetime.datetime.today().date()  #方便的函数转换成字符串
    return str(day) 


def get_year():
    year = datetime.datetime.today().year
    return year


def get_month():
    month = datetime.datetime.today().month
    return month

def get_hour():
    return datetime.datetime.today().hour
    
    
def today_last_year():  #去年今日
    lasty = datetime.datetime.today().date() + datetime.timedelta(-365)
    return str(lasty)


def day_last_week(days=-7):  #上周今日
    lasty = datetime.datetime.today().date() + datetime.timedelta(days)
    return str(lasty)


def get_now():    
    return time.strftime('%Y-%m-%d %H:%M:%S')   #返回当前时间字符串


def int2time(timestamp):
    datearr = datetime.datetime.utcfromtimestamp(timestamp)
    timestr = datearr.strftime("%Y-%m-%d %H:%M:%S")
    return timestr


def diff_day(start=None, end=None):
    d1 = datetime.datetime.strptime(end, '%Y-%m-%d')
    d2 = datetime.datetime.strptime(start, '%Y-%m-%d')
    delta = d1 - d2
    return delta.days   #返回日期差额


def get_quarts(start, end):
    idx = pd.period_range('Q'.join(year_qua(start)), 'Q'.join(year_qua(end)),
                          freq='Q-JAN')  #根据2015Q2，2015Q3和频率获取PeriodIndex
    return [str(d).split('Q') for d in idx][::-1] #产生一个倒序的每日日期,如果是正数就是正序，日期间隔就是1


def trade_cal():
    '''
            交易日历
    isOpen=1是交易日，isOpen=0为休市
    '''
    df = pd.read_csv(ct.ALL_CAL_FILE)  #'http://file.tushare.org/tsdata/calAll.csv'
    return df


def is_holiday(date):
    '''
            判断是否为交易日，返回True or False
    '''
    df = trade_cal()
    holiday = df[df.isOpen == 0]['calendarDate'].values  #假期数组
    if isinstance(date, str):  
        today = datetime.datetime.strptime(date, '%Y-%m-%d')

    if today.isoweekday() in [6, 7] or date in holiday:
        return True
    else:
        return False


def last_tddate():   #昨天
    today = datetime.datetime.today().date()
    today=int(today.strftime("%w"))
    if today == 0:
        return day_last_week(-2)
    else:
        return day_last_week(-1)
        

def tt_dates(start='', end=''):
    startyear = int(start[0:4])
    endyear = int(end[0:4])
    dates = [d for d in range(startyear, endyear+1, 2)]
    return dates
    
    
def _random(n=13):  #n位的随机数
    from random import randint
    start = 10**(n-1)
    end = (10**n)-1
    return str(randint(start, end))

def get_q_date(year=None, quarter=None):  #返回每个季度最后一天
    dt = {'1': '-03-31', '2': '-06-30', '3': '-09-30', '4': '-12-31'}
    return '%s%s'%(str(year), dt[str(quarter)])

