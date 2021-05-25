#!/usr/bin/env python3
"""
This is a quick script to process the sitemap on help.sumologic.com
"""

import xmltodict
import requests
from bs4 import BeautifulSoup

SITE_MAP = "https://help.sumologic.com/sitemap.xml"

my_xml = requests.get(SITE_MAP).text
my_dict = xmltodict.parse(my_xml)

def get_meta_char(url_base):
    """
    This function parses a given page for metadata strings
    """
    url_target = url_base + "#rules"
    url_contents = requests.get(url_target).text
    soup = BeautifulSoup(url_contents, features="lxml")
    selector = 'ul strong'
    quotes = soup.select(selector)
    varlist = list()
    for quote in quotes:
        varlist.append(quote.text)
    return varlist

for url in my_dict['urlset']['url']:
    location = url['loc']
    lastmod = url['lastmod']
    frequency = url['changefreq']
    verb = location.rsplit('/', 1)[-1]
    if 'Operators' in location:
        variables = get_meta_char(location)
        metadata = list()
        if len(variables) == 0:
            metadata.append('none')
        else:
            for variable in variables:
                if '_' in variable:
                    print('{:16} {:30} {}'.format(verb, variable, location))
