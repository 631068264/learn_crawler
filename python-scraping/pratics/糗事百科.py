#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/9/7 18:02
@annotation = '' 
"""
import urllib2

import re

page = 3
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
headers = {'User-Agent': user_agent}
url = 'http://www.qiushibaike.com/hot/page/%s' % (page,)
try:
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    content = response.read().decode('utf-8')
    pattern = re.compile(
        '<div.*?author.*?">.*?<a.*?<img src="(.*?)"' +
        '.*?</a>.*?<a.*?title="(.*?)">.*?' +
        '<div.*?content.*?<span>(.*?)</span>.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',
        re.S)

    items = re.findall(pattern, content)

    for item in items:
        haveImg = re.search("img", item[3])
        if not haveImg:
            print item[0], item[1], item[2], item[4]


except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    if hasattr(e, "reason"):
        print e.reason
