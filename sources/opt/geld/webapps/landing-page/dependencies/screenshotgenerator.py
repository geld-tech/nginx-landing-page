#!/usr/bin/env python
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def take_screenshot(url, filename="screenshot.png"):
    browser = None
    result = False
    try:
        chromium_webdriver_path = r"/usr/lib/chromium-browser/chromedriver"
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("window-size=1024,768")
        chrome_options.add_argument("--no-sandbox")
        browser = webdriver.Chrome(executable_path=chromium_webdriver_path, chrome_options=chrome_options)
        browser.get(url)
        result = browser.save_screenshot(filename)
    except Exception, e:
        print "Exception: %s" % e 
    finally:
        if browser:
            browser.quit()
        return result

def generate_screenshots(data, file_prefix="screenshot", dir_path="/tmp"):
    increment = 1
    for location in data:
        file_path = "%s/%s%s.png" % (dir_path, file_prefix, increment)
        success = take_screenshot(data[location], file_path)
        increment += 1
        if not success:
            print "Could not create %s" % file_path
