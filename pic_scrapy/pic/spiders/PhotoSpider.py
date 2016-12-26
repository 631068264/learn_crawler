#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/10/24 15:01
@annotation = '' 
"""
from urlparse import urljoin

import scrapy
from pic.items import PhotoItem


class PhotoSpider(scrapy.Spider):
    start_urls = ["https://www.610hu.com/htm/girl.htm"]
    name = "photo"
    domain = "https://www.610hu.com"

    def parse(self, response):
        tds = response.css("table td")
        for td in tds:
            href = urljoin(self.domain, td.xpath("a/@href").extract_first())
            dic = td.css("img").xpath("@src").re_first(r".*/(.*?)\.gif")
            yield scrapy.Request(href, callback=self.parse_page, meta={"photo_name": dic})

    def parse_page(self, response):
        page_num = response.css(".pages strong").xpath("text()").re_first(r"/(\d?)")
        if page_num:
            for page in page_num:
                yield scrapy.Request(urljoin(response.url, ("%s.htm" % page)), callback=self.parse_charter,
                                     meta={"photo_name": response.meta["photo_name"]})

    def parse_charter(self, response):
        lis = response.css("ul.movieList li")
        links = []
        for li in lis:
            charter_link = urljoin(self.domain, li.xpath("a/@href").extract_first())
            charter_name = li.css("h3").xpath("text()").extract_first()
            charter_time = li.css("span").xpath("text()").extract_first()
            links.append(scrapy.Request(charter_link,
                                        callback=self.parse_detail,
                                        meta={
                                            "photo_name": response.meta["photo_name"],
                                            "charter_link": charter_link,
                                            "charter_name": charter_name,
                                            "charter_time": charter_time,
                                        }))
        return links

    def parse_detail(self, response):
        imgs = response.css(".picContent img")
        items = []
        for img in imgs:
            src = img.xpath("@src").extract_first()
            item = PhotoItem({
                "photo_name": response.meta["photo_name"],
                "charter_link": response.meta["charter_link"],
                "charter_name": response.meta["charter_name"],
                "charter_time": response.meta["charter_time"],
                "img_url": src,
            })
            items.append(item)
        return items
