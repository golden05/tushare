#!/usr/bin/env python
# -*- coding:utf-8 -*- 

'''
Created on 2016年10月1日
@author: Jimmy Liu
@group : waditu
@contact: jimmysoa@sina.cn
'''

import json
import time
import six   #提供python 2 和 3 的兼容库
from tushare.trader import vars as vs

def nowtime_str():
    return time.time() * 1000


def get_jdata(txtdata):
    txtdata = txtdata.content
    if six.PY3:    #判断当前代码使用的是python3
        txtdata = txtdata.decode('utf-8')
    jsonobj = json.loads(txtdata)  #反序列转换为python对象
    return jsonobj
        
        
def get_vcode(broker, res):
    from PIL import Image
    import pytesseract as pt  #OCR光学字符识别,读取图像文件解码成可读的文件识别验证码
    import io
    if broker == 'csc':
        imgdata = res.content
        img = Image.open(io.BytesIO(imgdata))  #读取二进制数据
        vcode = pt.image_to_string(img)    #读取Image对象到字符串
        return vcode
    
