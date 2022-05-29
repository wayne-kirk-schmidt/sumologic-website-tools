#!/usr/bin/env python3
"""
This is a quick script to process the sitemap on help.sumologic.com
"""

import xmltodict
import requests

SITE_MAP = "https://help.sumologic.com/sitemap.xml"

my_xml = requests.get(SITE_MAP).text
my_dict = xmltodict.parse(my_xml)

operators = {}

for url in my_dict['urlset']['url']:
    location = url['loc']
    lastmod = url['lastmod']
    frequency = url['changefreq']
    verb = location.rsplit('/', 1)[-1]
    verb = verb.replace("()","")
    if 'Operators' in location:
        if '-' not in verb:
            operators[verb] = location

for mykey, myvalue in operators.items():
    print(f'{mykey},{myvalue}')
