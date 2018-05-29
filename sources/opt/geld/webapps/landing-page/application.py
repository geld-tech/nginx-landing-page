#!/usr/bin/env python
import glob
from flask import Flask, render_template

sys.path.append('/opt/geld/webapps/landing-page/dependencies')
from nginxparser import load

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
	try:
		chromium_webdriver_path = r"/usr/lib/chromium-browser/chromedriver"
		chrome_options = Options()
		chrome_options.add_argument("--headless")
		browser = webdriver.Chrome(executable_path=chromium_webdriver_path,
					 chrome_options=chrome_options)
		browser.get(url)
		screenshot = browser.save_screenshot(filename)
	finally:
		if browser:
			browser.quit()

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

