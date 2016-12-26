#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/9/21 12:41
@annotation = '' 
"""
import os

project_home = os.path.realpath(__file__)
project_home = os.path.split(project_home)[0]

import sys

sys.path.append(os.path.split(project_home)[0])
sys.path.append(project_home)

from http.cookiejar import LWPCookieJar
import tesserocr
import functools
import io
import random
import requests
from PIL import Image
from base import util, logger, config
from base.util import chrome_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class AnswerSpider(object):
    url = "http://www.beeang.com/forum.php?mod=viewthread&tid=1603&extra=page%3D1"
    domain = "http://www.beeang.com/forum.php"
    access = functools.partial(util.access, domain=domain)
    log = logger.get("spider")
    error = logger.get("error").error

    # driver = util.get_driver()
    # wait = WebDriverWait(driver, 5)

    def run(self):
        # with chrome_driver(self.url) as driver:
        #     driver.find_element_by_partial_link_text("回复").click()
        #     try:
        #         WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "subjecthide")))
        #     except Exception:
        #         print(util.error_msg())
        #         # self._login(driver)
        #     finally:
        #         # print(driver.find_element_by_id("subjecthide").text)
        #         pass
        self._login()

    def _login(self):
        with chrome_driver(self.domain) as driver:
            driver.find_element_by_css_selector("button.pn.vm").click()
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "fwin_content_login")))
            except Exception:
                print("error")
            finally:
                driver.find_element_by_name("username").clear()
                driver.find_element_by_name("username").send_keys("631068264")
                driver.find_element_by_name("password").clear()
                driver.find_element_by_name("password").send_keys("wuyuxi08")

                # qrcode_url = driver.find_element_by_css_selector("img.vm")
                qrcode = self._get_qrcode(driver)
                driver.find_element_by_name("seccodeverify").send_keys("fafa")
                # qrcode.send_keys(Keys.RETURN)

    def _get_qrcode(self, driver):
        # driver.find_element_by_partial_link_text("换一个").click()
        url = driver.find_element_by_css_selector("[id~='vseccode']>img").get_attribute("src")
        print(url)
        response = requests.get(url)
        qrcode = tesserocr.image_to_text(Image.open(io.BytesIO(response.content)))
        print(qrcode)
        return qrcode


def login():
    url = "http://www.beeang.com/home.php?mod=space&do=notice"
    domain = "http://www.beeang.com/"
    mics_url = domain + "misc.php"

    session = requests.session()
    session.cookies = LWPCookieJar("../logs/cookie.txt")
    # session.cookies.load()

    # print(session.cookies["ggrZ_2132_sid"])
    r = session.get(url, headers=config.headers)
    # session.cookies.save()
    payload = {
        "mod": "seccode",
        "update": random.randint(10000, 99999),
        "idhash": "cSA%s" % r.cookies["ggrZ_2132_sid"],
    }
    print(payload)
    # session.cookies.load()
    headers = util.get_headers({"Referer": url})
    r = session.get(mics_url, headers=headers, params=payload)
    captcha_image = Image.open(io.BytesIO(r.content))
    captcha_image.save('Captcha.png')

    # print(tesserocr.tesseract_version())  # print tesseract-ocr version

    # print(tesserocr.get_languages())  # prints tessdata path and list of available languages
    print(tesserocr.image_to_text(captcha_image))
    # qrcode = pytesseract.image_to_string(captcha_image)
    # print(qrcode)

    # AIzaSyBzeghi0W7mGczap8SC8AmNudYOlwfU-KE

    # cookie = session.cookies.load("../logs/cookie.txt", ignore_discard=True, ignore_expires=True)
    # print(cookie)


if __name__ == '__main__':
    # log setting
    # logger.init_log([(n, os.path.join("logs", p), l)
    #                  for n, p, l in config.log_config])
    # spider = AnswerSpider()
    # spider.run()
    login()
