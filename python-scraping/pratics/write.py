#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/9/8 10:25
@annotation = '' 
"""
import os
import urllib


def saveImg(self, imageURL, fileName):
    u = urllib.urlopen(imageURL)
    data = u.read()
    f = open(fileName, 'wb')
    f.write(data)
    f.close()


def saveBrief(self, content, name):
    fileName = name + "/" + name + ".txt"
    f = open(fileName, "w+")
    print u"正在偷偷保存她的个人信息为", fileName
    f.write(content.encode('utf-8'))


def mkdir(self, path):
    path = path.strip()
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False
