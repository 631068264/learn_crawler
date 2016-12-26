#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/9/15 17:44
@annotation = '' 
"""
import os
import re

from base import util, logger, config
from peewee import IntegrityError
from pic.db import redis_conn as redis, db
from pic.models import Manga, Page
from pyquery import PyQuery as pq


class PicSpider(object):
    # TODO:异步request
    pic_url = "http://www.177pic66.com"
    domain = "http://www.177pic66.com"

    log = logger.get("spider")
    error = logger.get("error").error
    pages_url = ""
    total_page = 0

    def run(self):
        self._get_main_page_total(self.pic_url)
        for index in range(1, self.total_page + 1):
            page_url = "%s/%s" % (self.pages_url, index)
            manga_list = self._parse_main_page(page_url)
            if manga_list is not None:
                for num, manga in enumerate(manga_list):
                    self.log.info("Crawling:(%s,%s)" % (index, num + 1))
                    self._parse_view_page(manga)
        self.log.info("Crawl_ALL: sussess")

    @db.atomic()
    def _parse_main_page(self, url=None):
        doc = util.access(url, domain=self.domain)
        if doc is None:
            return None

        manga_list = doc('div.post_box')
        if len(manga_list) == 0:
            self.error("main_page manga_list None [url: %s]" % url)
        items = []
        for manga in manga_list:
            manga = pq(manga)
            item = {
                "manga_id": int(manga("div.c-top").attr.id.split("-")[-1]),
                "cover_url": manga("img").attr.src,
                "view_page": manga("a.disp_a").attr.href,
                "title": manga("div.tit h2 a").text(),
                "date": util.str_date(manga("div.datetime").remove("br").text(), format="%Y %m-%d"),
            }
            if redis.exists("url:%s" % item["view_page"]):
                continue
            # print(item)
            items.append(item)
        if items:
            try:
                # TODO:ignore
                Manga.insert_many(items).execute()
                return items
            except IntegrityError as e:
                manga_id = int(re.match(r'^\(.*?\'(.*?)\'.*?\)$', str(e)).group(1))
                for item in items:
                    if item["manga_id"] == manga_id:
                        self._parse_view_page(item)
                        self.log.info("Fix [id: %s]" % manga_id)
                        break
        return None

    @db.atomic()
    def _parse_view_page(self, manga):
        view_page_url = manga.get("view_page")
        # url 去重
        doc = util.access(view_page_url, unique=True, domain=self.domain)
        if doc is None:
            return None
        page_count = int(doc("div.wp-pagenavi p a:last").prev("a span").text())

        items = []
        page_num = 0
        page_total = 0
        try:
            for index in range(1, page_count + 1):
                doc = util.access("%s/%s" % (view_page_url, index), unique=True, domain=self.domain)
                if doc is None:
                    continue
                img_list = [pq(imgs).attr.src for imgs in doc("div.entry-content img")]
                page_total += len(img_list)
                for img_url in img_list:
                    page_num += 1
                    item = {
                        "manga_id": manga["manga_id"],
                        "page_num": page_num,
                        "img_url": img_url,
                    }
                    # self.log.info("Crawling:[id: %s ,page: %s/%s]" % (item["manga_id"], page_num,page_total))
                    # print(item)
                    items.append(item)

            if not items:
                self.log.error(
                    "ERROR:[id: %s ,page: %s/%s]:%s" % (
                        manga["manga_id"], page_num, page_total, "%s html解析有误" % view_page_url))
                return None
            Page.insert_many(items).execute()
            self.log.info("Crawl_Finish:[id: %s ,page: %s/%s]" % (manga["manga_id"], page_num, page_total))
        except Exception as e:
            self.log.error(
                "ERROR:[id: %s ,page: %s/%s]:%s" % (manga["manga_id"], page_num, page_total, util.error_msg()))

    def _get_main_page_total(self, url=None):
        doc = util.access(url, domain=self.domain)
        if doc is None:
            return
        groups = doc("div.wp-pagenavi > a:last").attr.href.split("/")
        self.total_page = int(groups.pop())
        self.pages_url = "/".join(groups)


if __name__ == '__main__':
    # log setting
    logger.init_log([(n, os.path.join("logs", p), l)
                     for n, p, l in config.log_config])
    try:
        spider = PicSpider()
        spider.run()
    except Exception:
        error = logger.get("error").error
        error(util.error_msg())
