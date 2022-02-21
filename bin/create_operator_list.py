#!/usr/bin/env python3
"""
This is a quick script to process the sitemap on help.sumologic.com
"""

import os
import time
import datetime
import re
import sys
import xmltodict
import requests
from bs4 import BeautifulSoup

SITE_MAP = "https://help.sumologic.com/sitemap.xml"

my_xml = requests.get(SITE_MAP).text
my_dict = xmltodict.parse(my_xml)

operators = dict()

for url in my_dict['urlset']['url']:
    location = url['loc']
    lastmod = url['lastmod']
    frequency = url['changefreq']
    verb = location.rsplit('/', 1)[-1]
    if 'Operators' in location:
        if ( '_' not in verb and '-' not in verb ):
            operators[verb] = location

for mykey, myvalue in operators.items():
    print('{},{}'.format(mykey, myvalue))
