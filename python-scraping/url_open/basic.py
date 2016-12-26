#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/9/7 15:25
@annotation = ''
"""
from urllib2 import urlopen

html = urlopen("http://www.pythonscraping.com/exercises/exercise1.html")
print(html.read())
