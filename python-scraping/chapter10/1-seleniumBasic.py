from selenium import webdriver
import time
DRIVER_BIN = "../bin/chromedriver_for_mac"
PHANTOMJS_BIN = "../bin/phantomjs_for_mac"

driver = webdriver.PhantomJS(executable_path=PHANTOMJS_BIN)
driver.get("http://pythonscraping.com/pages/javascript/ajaxDemo.html")
time.sleep(3)
print(driver.find_element_by_id("content").text)
driver.close()