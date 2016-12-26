#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/5/27 13:02
@annotation = '' 
"""


def covert_column_name(string):
    return " `%s` " % string


def quote(string):
    return "\"%s\"" % string


def comment(string):
    return "'%s'" % string
