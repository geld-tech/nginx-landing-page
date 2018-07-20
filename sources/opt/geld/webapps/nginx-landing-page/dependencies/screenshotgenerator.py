#!/usr/bin/env python
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image

def take_screenshot(url, filename="screenshot.png", width="1024", height="768", load_time=10):
    browser=None
    result=False
    title=''
    description=''
    try:
        chromium_webdriver_path = r"/usr/lib/chromium-browser/chromedriver"
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--hide-scrollbars")
        chrome_options.add_argument("window-size=%s,%s" % (width, height))
        browser = webdriver.Chrome(executable_path=chromium_webdriver_path, chrome_options=chrome_options)
        browser.get(url)
        time.sleep(load_time)
        title = browser.title
        description = browser.find_element_by_xpath("//meta[@name='description']").get_attribute("content")
        result = browser.save_screenshot(filename)
    except Exception, e:
        print "Exception: %s" % e 
    finally:
        if browser:
            browser.quit()
        return result, title, description

def resize_picture(infile, outfile, file_ext="JPEG", width=128, height=128):
    im=None
    success=False
    try:
        with Image.open(infile) as im:
            size = int(width), int(height)
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(outfile, file_ext)
        success=True
    finally:
        return success

def generate_screenshots(data, file_prefix="screenshot", file_ext="png", dir_path="/tmp", generate_thumbnails=False, thumb_width=128, thumb_height=128):
    screenshots=[]
    increment=1
    for location in data:
        file_path = "%s%s.%s" % (file_prefix, increment, file_ext)
        success, title, description = take_screenshot(data[location], dir_path+"/"+file_path)
        increment += 1
        if success:
            screenshot = {"title": title, "description": description, "url": location, "screenshot": file_path}
            if generate_thumbnails:
                    thumb_path = "%s%s-thumb.%s" % (file_prefix, increment, file_ext)
                    if resize_picture(file_path, thumb_path, file_ext, thumb_width, thumb_height):
                        screenshot["thumbnail"] = thumb_path
                    else:
                        print "Could not create thumb %s" % file_thumb
            screenshots.append(screenshot)
        else:
            print "Could not create %s" % file_path
    return screenshots

