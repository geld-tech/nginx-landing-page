#!/usr/bin/env python
import glob, json, os, sys
from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from dependencies.nginxparser import load
import dependencies.nginxconfigparser as nginxconfig
import dependencies.screenshotgenerator as screenshot


# Globals
NGINX_CONFD_FILES="/etc/nginx/conf.d/*.conf"
DATA_DIR=os.path.dirname(os.path.realpath(__file__))+"/static/data/"
DATA_JSON=DATA_DIR+"websites.json"


# Functions
def load_websites_data(data_json):
	data = []
	if os.path.exists(data_json):
		with open(data_json) as infile:
			data = json.load(infile)
	return data


# Start Flask Application
app = Flask(__name__)
app.debug=True


# Flask App and Routes
@app.route("/")
@app.route("/<section>")
def index(section=None):
	page_title="__PACKAGE_NAME__"
	page_domain="__PACKAGE_DOMAIN__"
	data=load_websites_data(DATA_JSON)
	return render_template('index.html', page_title=page_title, page_domain=page_domain, section=section, data=data)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

if __name__ == "__main__":
	locations = parse_nginx_config_files(NGINX_CONFD_FILES)
		
	app.run(host='0.0.0.0')

