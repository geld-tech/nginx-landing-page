#!/usr/bin/env python
import glob, os, sys 
from dependencies.nginxparser import load

NGINX_CONFD_FILES = "/etc/nginx/conf.d/*.conf"

def parse_config(input, data):
    if isinstance(input, list):
        if len(input)  == 2 and not isinstance(input[0], list):
            data[input[0]] = input[1]
        else:
            for item in input:
                parse_config(item, data)

def parse_nginx_config_files(directory):
    locations = {}
    nginx_config_files = glob.glob(directory)
    for config_file in nginx_config_files:
        nginx_config_data = {}
        location = destination = ''
        nginx_config_contents = load(open(config_file))
        parse_config(nginx_config_contents, nginx_config_data)
        if nginx_config_data.has_key('location'):
            location = nginx_config_data.get('location')
        if nginx_config_data.has_key('proxy_pass'):
            destination = nginx_config_data.get('proxy_pass')
        locations[location] = destination
    return locations

# Main
if __name__ == "__main__":
    locations = parse_nginx_config_files(NGINX_CONFD_FILES)
    print locations
