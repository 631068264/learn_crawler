#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/11/3 09:49
@annotation = '' 
"""


def test(response, name="test.html"):
    print (response.url)
    with open(name, "wb") as f:
        f.write(response.body)


def print_tag(tag):
    print (tag.xpath("*").extract())
