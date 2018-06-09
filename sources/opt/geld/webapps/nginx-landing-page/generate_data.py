#!/usr/bin/env python
import glob, json, os, sys

from dependencies.nginxparser import load
import dependencies.nginxconfigparser as nginxconfig
import dependencies.screenshotgenerator as screenshot


# Globals
NGINX_CONFD_FILES="/etc/geld/nginx.conf.d/*.conf"
DATA_DIR=os.path.dirname(os.path.realpath(__file__))+"/static/data/"
DATA_JSON=DATA_DIR+"websites.json"


# Functions
def generate_screenshots_from_nginxconfig(nginx_confd_files, dir_path, data_json):
	locations = nginxconfig.parse_nginx_config_files(nginx_confd_files)
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	screenshots = screenshot.generate_screenshots(locations, file_prefix="screenshot-", dir_path=dir_path)
	with open(data_json, 'w') as outfile:
		json.dump(screenshots, outfile)

def load_websites_data(data_json):
	with open(data_json) as infile:
		data = json.load(infile)
	return data


if __name__ == "__main__":
    generate_screenshots_from_nginxconfig(NGINX_CONFD_FILES, DATA_DIR, DATA_JSON)
