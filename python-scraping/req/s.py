#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/9/10 12:24
@annotation = '' 
"""
import requests

# 要想检查某个主机的SSL证书，你可以使用 verify 参数 默认情况下 verify 是 True
r = requests.get('https://kyfw.12306.cn/otn/', verify=False)
print r.text

proxies = {
    "https": "http://41.118.132.69:4433"
}
r = requests.post("http://httpbin.org/post", proxies=proxies)
print r.text
