#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/9/7 15:09
@annotation = '' 
"""
# post方法
import urllib
import urllib2

values = {"username": "1016903103@qq.com", "password": "XXXX"}
data = urllib.urlencode(values)
url = "https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn"
request = urllib2.Request(url, data)
response = urllib2.urlopen(request, timeout=10)
print response.read()
