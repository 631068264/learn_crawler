#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/9/7 16:28
@annotation = '' 
"""
import urllib2

response = urllib2.urlopen("https://www.baidu.com")
print response.read()
"""
cookie 保存到变量
"""
import cookielib
import urllib2

# 声明一个CookieJar对象实例来保存cookie
cookie = cookielib.CookieJar()
# 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
handler = urllib2.HTTPCookieProcessor(cookie)
# 通过handler来构建opener
opener = urllib2.build_opener(handler)
# 此处的open方法同urllib2的urlopen方法，也可以传入request
response = opener.open('http://www.baidu.com')

for item in cookie:
    print 'Name = ' + item.name
    print 'Value = ' + item.value

"""
cookie 保存到文件
"""
import cookielib
import urllib2

# 设置保存cookie的文件，同级目录下的cookie.txt
filename = 'cookie.txt'
# 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
cookie = cookielib.MozillaCookieJar(filename)
# 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
handler = urllib2.HTTPCookieProcessor(cookie)
# 通过handler来构建opener
opener = urllib2.build_opener(handler)
# 创建一个请求，原理同urllib2的urlopen
response = opener.open("http://www.baidu.com")
# 保存cookie到文件
cookie.save(ignore_discard=True, ignore_expires=True)

"""
获取cookie并使用
"""
import cookielib
import urllib2

# 创建MozillaCookieJar实例对象
cookie = cookielib.MozillaCookieJar()
# 从文件中读取cookie内容到变量
cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
# 创建请求的request
req = urllib2.Request("http://www.baidu.com")
# 利用urllib2的build_opener方法创建一个opener
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
response = opener.open(req)
print response.read()


"""

"""
import urllib
import urllib2
import cookielib

filename = 'cookie.txt'
# 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
cookie = cookielib.MozillaCookieJar(filename)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
postdata = urllib.urlencode({
    'stuid': '201200131012',
    'pwd': '23342321'
})
# 登录教务系统的URL
loginUrl = 'http://jwxt.sdu.edu.cn:7890/pls/wwwbks/bks_login2.login'
# 模拟登录，并把cookie保存到变量
result = opener.open(loginUrl, postdata)
# 保存cookie到cookie.txt中
cookie.save(ignore_discard=True, ignore_expires=True)
# 利用cookie请求访问另一个网址，此网址是成绩查询网址
gradeUrl = 'http://jwxt.sdu.edu.cn:7890/pls/wwwbks/bkscjcx.curscopre'
# 请求访问成绩查询网址
result = opener.open(gradeUrl)
print result.read()