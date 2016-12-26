#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/9/7 15:25
@annotation = '' 
"""
import urllib2
httpHandler = urllib2.HTTPHandler(debuglevel=1)
httpsHandler = urllib2.HTTPSHandler(debuglevel=1)

enable_proxy = True
proxy_handler = urllib2.ProxyHandler({"http" : '216.174.135.183:8080'})
null_proxy_handler = urllib2.ProxyHandler({})
if enable_proxy:
    opener = urllib2.build_opener(proxy_handler,httpHandler,httpsHandler)
else:
    opener = urllib2.build_opener(null_proxy_handler)
# urllib2.install_opener(opener)
html = opener.open("https://www.baidu.com/")
print(html.read())