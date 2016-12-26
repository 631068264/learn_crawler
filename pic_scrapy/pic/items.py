# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


import scrapy


class ProxyItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()
    position = scrapy.Field()
    type = scrapy.Field()
    speed = scrapy.Field()
    last_check_time = scrapy.Field()


class PhotoItem(scrapy.Item):
    photo_name = scrapy.Field()
    charter_link = scrapy.Field()
    charter_name = scrapy.Field()
    charter_time = scrapy.Field()
    img_url = scrapy.Field()
