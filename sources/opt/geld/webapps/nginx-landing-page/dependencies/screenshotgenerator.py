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
        chrome_options.add_argument("--disable-setuid-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument('--user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"')
        chrome_options.add_argument("--hide-scrollbars")
        chrome_options.add_argument("window-size=%s,%s" % (width, height))

        # Chromium and/or WebDriver can become broken during updates or distribution upgrades.
        # One of the possible solution to fix these issues was do downgrade the following packages (download .deb files and install locally with `sudo apt install ./chromium-*`):
        #   - chromium-browser
        #   - chromium-browser-l10n
        #   - chromium-chromedriver
        #   - chromium-codecs-ffmpeg-extra
        #
        # Tested versions (on Ubuntu 16.04.1 and 16.04.2) are:
        #   - 65.0.3325.181
        #   - 66.0.3359.181
        #
        browser = webdriver.Chrome(executable_path=chromium_webdriver_path, chrome_options=chrome_options, service_args=["--verbose", "--log-path=/tmp/chromium_webdriver.log"])
        browser.get(url)
        time.sleep(load_time)

        title = browser.title
        if (browser.find_element_by_xpath("//meta[@name='description']")):
            description = browser.find_element_by_xpath("//meta[@name='description']").get_attribute("content")
        result = browser.save_screenshot(filename)
    except Exception, e:
        print "Exception: %s" % e 
    finally:
        if browser:
            browser.close()
            browser.quit()
            del browser
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

