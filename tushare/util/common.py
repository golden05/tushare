#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
Created on 2015年7月31日
@author: Jimmy Liu
@group: DataYes Data.dept
@QQ:52799046
"""

try:
    from httplib import HTTPSConnection
except ImportError:
    from http.client import HTTPSConnection  #试图适配2.7 和3.x版本
import urllib  #核心模块自动提供http ftp统一客户端接口  
from tushare.util import vars as vs  #引入常用常量
from tushare.stock import cons as ct    #引入stock目录下的cons文件 常量

class Client:
    httpClient = None
    def __init__(self , token):
        self.token = token
        self.httpClient = HTTPSConnection(vs.HTTP_URL, vs.HTTP_PORT) #安全连接通联网站
                                                #https://api.wmcloud.com:443  
        
    def __del__( self ):
        if self.httpClient is not None:
            self.httpClient.close()
            
            
    def encodepath(self, path):   #编码
        start = 0
        n = len(path) #一个字符串的长度
        re = ''
        i = path.find('=', start) #从start位置开始寻找=字符在第几位
        while i != -1 :    #-1就是没找到，当找到了
            re += path[start:i+1]  #把找到的字符从start开始赋值加到re变量
            start = i+1
            i = path.find('&', start)  #从接下来的位置找到出现&的位置
            if(i>=0):
                for j in range(start, i):  在这个范围内循环
                    if(path[j] > '~'): 
                        if ct.PY3:   #兼容2.版本
                            re += urllib.parse.quote(path[j])
                        else:
                            re += urllib.quote(path[j])
                    else:
                        re += path[j]  
                re += '&'
                start = i+1
            else:
                for j in range(start, n):
                    if(path[j] > '~'):
                        if ct.PY3:   #在python3版本下
                            re += urllib.parse.quote(path[j]) #解析参数
                        else:
                            re += urllib.quote(path[j])
                    else:
                        re += path[j]  
                start = n
            i = path.find('=', start)
        return re  #返回字符串
    
    
    def init(self, token):
        self.token = token
        
        
    def getData(self, path):
        result = None
        path='/data/v1' + path
        path=self.encodepath(path)
        try:
            self.httpClient.request('GET', path,
                                    headers = {"Authorization": "Bearer " + self.token})
            response = self.httpClient.getresponse()
            if response.status == vs.HTTP_OK:  #200
                result = response.read()
            else:
                result = response.read()
            if(path.find('.csv?') != -1):
                result=result.decode('GBK').encode('utf-8')  #解码GBK 转换 utf-8
            return response.status, result
        except Exception as e
            raise e
        return -1, result
