#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/6/21 11:11
@annotation = '' 
"""
import time
import config_global.default as config
from base import logger, smartpool, poolmysql
from base.decorator import db_conn
from bs4 import BeautifulSoup
from selenium import webdriver
from base.smartsql import Table as T, Field as F, QuerySet as QS, Expr as E


@db_conn("db_writer")
def db(db_writer):
    # driver = webdriver.Chrome("/usr/local/bin/chromedriver")
    driver = webdriver.PhantomJS(executable_path="/Users/wyx/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs")
    driver.get("http://adarsha.dharma-treasure.org/adarsha2016/#sid=T3256&db=tengyur")
    time.sleep(10)

    bsObj = BeautifulSoup(driver.page_source)
    tars = []
    for sibling in bsObj.find("div", {"id": "contents"}).div.next_siblings:
        print(sibling)
        s = {
            "title": sibling.h2.get_text(),
            "content": sibling.p.get_text(),
        }
        tars.append(s)

    driver.close()
    field_list = ("title", "content")
    QS(db_writer).table(T.crawl).insert_many(field_list, [[tar[key] for key in field_list] for tar in tars])
    print(tars)


if __name__ == "__main__":
    for name, setting in config.db_config.iteritems():
        smartpool.init_pool(
            name, setting, poolmysql.MySQLdbConnection, *config.db_conn_pool_size,
            maxidle=config.db_connection_idle, clean_interval=config.db_pool_clean_interval
        )

    db()
