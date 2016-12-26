#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/9/10 22:27
@annotation = '' 
"""
import time

from selenium import webdriver

DRIVER_BIN = "../bin/chromedriver_for_mac"
PHANTOMJS_BIN = "../bin/phantomjs_for_mac"

# driver = webdriver.Chrome(executable_path=DRIVER_BIN)
driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs")
driver.get("http://pythonscraping.com/pages/javascript/ajaxDemo.html")
time.sleep(3)
print(driver.find_element_by_id("content").text)
driver.quit()
