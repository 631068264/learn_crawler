#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/9/17 11:45
@annotation = '' 
"""
import os

log_config = [
    ["peewee", 'query.log', 'debug'],
    ["spider", 'spider.log', 'debug'],
    ["error", 'error.log', 'debug'],
]
redis_config = {
    "max_connections": 4,
    "host": 'localhost',
    "port": 6379,
    "db": 0,
    "password": None,
}
db_config = {
    "user": "root",
    "passwd": "wuyuxi08",
    "port": 3306,
    "max_connections": 20,
    "stale_timeout": 300,
}

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
proxies = {"http": "http://127.0.0.1:8087", "https": "https://127.0.0.1:8087"}
headers = {
    # "Referer": None,
    "User-Agent": user_agent,
}

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
CHROME_BIN = os.path.join(PROJECT_ROOT, '../bin/chromedriver_for_mac')
PHANTOMJS_BIN = os.path.join(PROJECT_ROOT, '../bin/phantomjs_for_mac')
PHONTOMJS_LOG_PATH = os.path.join(PROJECT_ROOT, '../logs/phantomjs.log')

