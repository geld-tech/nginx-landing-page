#!/usr/bin/env python
import glob, sys
from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from dependencies.nginxparser import load
import dependencies.nginxconfigparser
import dependencies.screenshotgenerator

# Globals
app = Flask(__name__)
app.debug=True

NGINX_CONFD_FILES = "/etc/nginx/conf.d/*.conf"
keypairs = {}


# Functions

def parse_config(input, data):
	if isinstance(input, list):
		if len(input)  == 2 and not isinstance(input[0], list):
			data[input[0]] = input[1]
	else:
		for item in input:
			parse_config(item, data)


def parse_nginx_config_files(directory):
	locations = []
	nginx_config_files = glob.glob(directory)
	for config_file in nginx_config_files:
		nginx_config_data = {}
		nginx_config_contents = nginxparser.load(open(config_file))
		parse_config(nginx_config_contents, nginx_config_data)
		if nginx_config_data.has_key('location'):
			locations.append(nginx_config_data.get('location'))
	return locations


def take_screenshot(url, filename="screenshot.png"):
	browser = None
	rc = False
	try:
		chromium_webdriver_path = r"/usr/lib/chromium-browser/chromedriver"
		chrome_options = Options()
		chrome_options.add_argument("--headless")
		browser = webdriver.Chrome(executable_path=chromium_webdriver_path,
					 chrome_options=chrome_options)
		browser.get(url)
		rc = browser.save_screenshot(filename)
	finally:
		if browser:
			browser.quit()
		return rc

def generate_screenshots(data, file_prefix="screenshot", dir_path="/tmp"):                     
    increment = 1
    for location in data:
        file_path = "%s/%s%s.png" % (dir_path, file_prefix, increment)                         
        success = take_screenshot(data[location], file_path)                                   
        increment += 1
        if not success:
            print "Could not create %s" % file_path                                            
            return False                                                                       

def generate_screenshots_from_nginxconfig():
    locations = parse_nginx_config_files(NGINX_CONFD_FILES)
    dir_path = os.path.dirname(os.path.realpath(__file__))+"/static/images/"                   
    if not os.path.exists(dir_path):                                                           
        os.makedirs(dir_path)
    generate_screenshots(locations, file_prefix="project_", dir_path=dir_path) 


# Flask App and Routes

@app.route("/")
@app.route("/<section>")
def index(section=None):
	page_title="geld.tech"
	return render_template('index.html', title=page_title, section=section)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

if __name__ == "__main__":
	locations = parse_nginx_config_files(NGINX_CONFD_FILES)
		
	app.run(host='0.0.0.0')

