#!/usr/bin/env python3
"""
This parses the sitemap to see what the relative ages are for the website
"""

import sys
import os
import datetime
import requests
import xmltodict

SITEURL = 'help.sumologic.com'
if len(sys.argv) > 1:
    SITEURL = sys.argv[1]

BASE_URL = 'https://' + SITEURL
SITE_MAP = 'https://' + SITEURL + '/' + 'sitemap.xml'

my_xml = requests.get(SITE_MAP).text

TODAY_DATE = datetime.date.today().strftime('%Y-%m-%d')

TD = TODAY_DATE.split('-')
nowdate = datetime.datetime.now()

my_dict = xmltodict.parse(my_xml)

for url in my_dict['urlset']['url']:
    fullurl = url['loc']
    fullpath = fullurl.replace(BASE_URL,'')
    dirname, filename = os.path.split(fullpath)
    lastmod = url['lastmod']
    frequency = url['changefreq']

    urldate = datetime.datetime.strptime(lastmod, "%Y-%m-%d")
    timedelta = (nowdate - urldate).days

    print(f'{lastmod},{timedelta},{frequency},{filename},{fullpath},{fullurl}')
