#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/9/10 16:27
@annotation = '' 
"""
from bs4 import BeautifulSoup

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title title1" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""
"""
<html>
 <head>
  <title>
   The Dormouse's story
  </title>
 </head>
 <body>
  <p class="title title1" name="dromouse">
   <b>
    The Dormouse's story
   </b>
  </p>
  <p class="story">
   Once upon a time there were three little sisters; and their names were
   <a class="sister" href="http://example.com/elsie" id="link1">
    <!-- Elsie -->
   </a>
   ,
   <a class="sister" href="http://example.com/lacie" id="link2">
    Lacie
   </a>
   and
   <a class="sister" href="http://example.com/tillie" id="link3">
    Tillie
   </a>
   ;
and they lived at the bottom of a well.
  </p>
  <p class="story">
   ...
  </p>
 </body>
</html>
"""
soup = BeautifulSoup(html, "lxml")

print soup.head.contents  # 子节点列表

# for child in soup.body.children:  # 直接子节点
#     print child
#
# for child in soup.p.descendants:  # 广度优先 遍历子节点
#     print child

# for string in soup.stripped_strings:  # 遍历节点内容
#     print(string)

# content = soup.head.title.string  # 遍历父节点
# for parent in content.parents:
#     print parent.name

# 兄弟节点
# print soup.p.next_sibling
#
# for tag in soup.p.next_siblings:
#     print tag

# 前后节点
print soup.head.next_element

print soup.p.previous_element.previous_element  # 空格 回车 会当成tag 坑爹啊

# for tag in soup.head.previous_elements:
#     print tag
