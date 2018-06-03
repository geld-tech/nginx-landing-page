#!/usr/bin/env python
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def take_screenshot(url, filename="screenshot.png", width="1024", height="768"):
    browser = None
    result = False
    try:
        chromium_webdriver_path = r"/usr/lib/chromium-browser/chromedriver"
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("window-size=%s,%s" % (width, height))
        browser = webdriver.Chrome(executable_path=chromium_webdriver_path,
                                chrome_options=chrome_options)
        browser.get(url)
        result = browser.save_screenshot(filename)
    except Exception, e:
        print "Exception: %s" % e 
    finally:
        if browser:
            browser.quit()
        return result

def generate_screenshots(data, file_prefix="screenshot", file_ext="png", dir_path="/tmp"):
    screenshots=[]
    increment=1
    for location in data:
        file_path = "%s%s.%s" % (file_prefix, increment, file_ext)
        success = take_screenshot(data[location], dir_path+"/"+file_path)
        increment += 1
        if success:
            screenshots.append({"url": location, "screenshot": file_path})
        else:
            print "Could not create %s" % file_path
    return screenshots

