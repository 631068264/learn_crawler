#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/10/21 21:05
@annotation = '' 
"""

import scrapy
from ..items import ProxyItem


class ProxySpider(scrapy.Spider):
    name = "proxy"
    allowed_domains = ["www.xicidaili.com"]

    def start_requests(self):
        reqs = []
        for page_num in range(1, 3):
            req = scrapy.Request("http://www.xicidaili.com/nn/%s" % page_num)
            reqs.append(req)
        return reqs

    def parse(self, response):
        trs = response.css("table#ip_list")[0].css("tr")

        items = []
        for tr in trs[1:]:
            # 只获取fast的代理
            if tr.xpath("td[7]/div/div[@class='bar_inner fast']/@class").extract_first():
                ip = tr.xpath("td[2]/text()").extract_first()
                port = tr.xpath("td[3]/text()").extract_first()
                position = tr.xpath("string(td[4])").extract_first().strip()
                type = tr.xpath("td[6]/text()").extract_first()
                speed = tr.xpath("td[7]/div[@class='bar']/@title").re_first(r"(\d*\.\d*)")
                last_check_time = tr.xpath("td[10]/text()").extract_first()

                item = ProxyItem({
                    "ip": ip,
                    "port": port,
                    "position": position,
                    "type": type,
                    "speed": speed,
                    "last_check_time": last_check_time,
                })

                items.append(item)
        return items
