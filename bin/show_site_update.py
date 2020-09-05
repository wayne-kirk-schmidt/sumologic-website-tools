#!/usr/bin/env python3
"""
This parses the sitemap to see what the relative ages are for the website
"""

import datetime
import requests
import xmltodict

SITE_MAP = "https://help.sumologic.com/sitemap.xml"

my_xml = requests.get(SITE_MAP).text

TODAY_DATE = datetime.date.today().strftime('%Y-%m-%d')

TD = TODAY_DATE.split('-')
today_date = datetime.date(int(TD[0]), int(TD[1]), int(TD[2]))

my_dict = xmltodict.parse(my_xml)

for url in my_dict['urlset']['url']:
    location = url['loc']
    lastmod = url['lastmod']
    frequency = url['changefreq']

    MD = lastmod.split('-')
    modify_date = datetime.date(int(MD[0]), int(MD[1]), int(MD[2]))

    date_delta = today_date - modify_date
    age = date_delta.days
    print('{},{},{},{}'.format(lastmod, age, frequency, location))
