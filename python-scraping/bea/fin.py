#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/9/10 17:30
@annotation = '' 
"""
from bs4 import BeautifulSoup

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title title1" name="dromouse"><b>The Dormouse's story</b></p>
<p class="title">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

soup = BeautifulSoup(html, "lxml")

# class 是 python 的关键词 recursive=False
print soup.find_all("a", class_="sister")

print soup.select("a")

# p中 查找#link1
print soup.select("p #link1")

# 子标签
print soup.select("head > title")

# 属性查找 属性和标签属于同一节点，所以中间不能加空格
print soup.select('a[class="sister"]')



# print type(soup.select('title'))
print soup.select('title')[0].get_text()

for title in soup.select('title'):
    print title.get_text()
