#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/9/15 21:24
@annotation = '' 
"""
import datetime
import pickle
import time

import requests
from base import config, cons
from pic.db import redis_conn as redis
from pyquery import PyQuery as pyquery


def str_time(data, format="%Y-%m-%d %H:%M:%S"):
    try:
        return datetime.datetime.strptime(data, format)
    except:
        return None


def str_date(data, format="%Y-%m-%d"):
    parsed = str_time(data, format)
    return None if parsed is None else parsed.date()


def time_str(data, format="%Y-%m-%d %H:%M:%S"):
    try:
        return datetime.datetime.strftime(data, format)
    except:
        return None


def get_headers(dic=None):
    d = config.headers
    if isinstance(dic, dict):
        d.update(dic)
        return d
    return d


def access(url, *, unique=False, domain=None):
    if unique:
        if redis.exists("url:%s" % url):
            # self.log.info("Ignore request: %s" % url)
            return None
        else:
            redis.set("url:%s" % url, 1)
    headers = get_headers({"Referer": domain}) if domain else get_headers()
    try:
        response = requests.get(url, headers=headers, proxies=config.proxies,
                                verify=False).text
    except Exception:
        raise ValueError(error_msg())
    return pyquery(response)


# def get_driver():
#     from selenium import webdriver
#     from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#
#     dcap = dict(DesiredCapabilities.PHANTOMJS)
#     dcap["phantomjs.page.settings.userAgent"] = config.user_agent
#
#     driver = webdriver.PhantomJS(executable_path=config.PHANTOMJS_BIN,
#                                  service_args=['--load-images=no'],
#                                  service_log_path=config.PHONTOMJS_LOG_PATH,
#                                  desired_capabilities=dcap)
#     return driver


class phantom_driver(object):
    def __init__(self, url):
        from selenium import webdriver
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = config.user_agent
        dcap["phantomjs.page.settings.cookie"] = config.cookie

        self.driver = webdriver.PhantomJS(executable_path=config.PHANTOMJS_BIN,
                                          service_args=['--load-images=no'],
                                          service_log_path=config.PHONTOMJS_LOG_PATH,
                                          desired_capabilities=dcap)
        self.url = url

    def __enter__(self):
        self.driver.get(self.url)
        # self.driver.add_cookie(get_cookie_dict())
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
        self.driver.quit()
        if exc_tb:
            raise ValueError(error_msg())


class chrome_driver(object):
    def __init__(self, url):
        from selenium import webdriver
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = config.user_agent
        # dcap["phantomjs.page.settings.cookie"] = config.cookie

        self.driver = webdriver.Chrome(executable_path=config.CHROME_BIN,
                                       service_args=['--load-images=no'],
                                       service_log_path=config.PHONTOMJS_LOG_PATH,
                                       desired_capabilities=dcap)
        self.url = url

    def __enter__(self):
        self.driver.get(self.url)
        # self.driver.add_cookie()
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        # self.driver.close()
        # self.driver.quit()
        if exc_tb:
            raise ValueError(exc_tb)


# def get_cookie_dict():
#     cookies = config.cookie.split(";")
#     cookie_dict = {}
#     for cookie in cookies:
#         group = cookie.split("=")
#         cookie_dict[group[0]] = group[1]
#     return cookie_dict


class LoginSession(object):
    def __init__(self):
        self.headers = None
        self.cookies = None

    @classmethod
    def load(cls, file_path):
        try:
            p = pickle.Unpickler(open(file_path, 'rb'))
            doc = p.load()

            obj = LoginSession()
            obj.headers = doc[cons.CACHE_HEADER_KEY]
            obj.cookies = doc[cons.CACHE_COOKIE_KEY]
            return obj
        except (KeyError, EOFError):
            return None

    def save(self, file_path):
        p = pickle.Pickler(open(file_path, 'wb'))
        p.dump({
            cons.CACHE_HEADER_KEY: self.headers,
            cons.CACHE_COOKIE_KEY: self.cookies,
        })


def get_time_ramdom():
    print(str(int(time.time())))


def error_msg():
    import traceback
    return traceback.format_exc()


if __name__ == '__main__':
    get_time_ramdom()
