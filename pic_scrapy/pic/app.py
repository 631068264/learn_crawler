#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/10/21 21:47
@annotation = '' 
"""

# def run_for_test(spider, **kwargs):
#     from scrapy.crawler import CrawlerProcess
#
#     process = CrawlerProcess({
#         'USER_AGENT': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
#         'DOWNLOADER_MIDDLEWARES': {
#             # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#             # 'pic.middlewares.RandomUserAgent': 500,
#             'pic.middlewares.ProxyMiddleware': 600,
#         }
#     })
#
#     process.crawl(spider, **kwargs)
#     process.start()

from scrapy import cmdline

cmdline.execute("scrapy crawl photo".split())
