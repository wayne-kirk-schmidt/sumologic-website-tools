#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This parses the sitemap to see what the relative ages are for the website
"""

import re
import sys
import os
import time
import datetime
import requests
import xmltodict
import hashlib
import urllib
import yaml

targetsitelist = [ 'help.sumologic.com', 'help.sumologic.jp' ]
nowdate = datetime.datetime.today()

siteresults = dict ()
sitesummary = dict ()

processing = 'summary'
if ( len(sys.argv) > 1):
    processing = sys.argv[1]

for targetsite in targetsitelist:
    baseurl = 'https://' + targetsite
    sitemap = 'https://' + targetsite + '/' + 'sitemap.xml'
    myxml = requests.get(sitemap).text
    dstamp = datetime.datetime.now().strftime('%Y%m%d')
    mydict = xmltodict.parse(myxml)

    for url in mydict['urlset']['url']:
        urlpath = url['loc']
        lastmod = url['lastmod']
        changes = url['changefreq']
        parse_object = urllib.parse.urlparse(urlpath)
        netpath = parse_object.path
        nethash = hashlib.md5(netpath.encode('utf-8')).hexdigest()
        netsite = parse_object.netloc
        urldate = datetime.datetime.strptime(lastmod, "%Y-%m-%d")
        timedelta = (nowdate - urldate).days
        if nethash not in siteresults:
            siteresults[nethash] = dict()
        if targetsite not in siteresults[nethash]:
            siteresults[nethash][targetsite] = dict()
        siteresults[nethash][targetsite]['time'] = timedelta
        siteresults[nethash][targetsite]['path'] = netpath

sitesummary['complete_tally'] = 0
sitesummary['common_pathnames'] = 0
for targetsite in targetsitelist:
    sitesummary[targetsite] = 0

for hash in siteresults:

    mykey = siteresults[hash].keys()
    mysite = (list(mykey)[0])
    mypath = siteresults[hash][mysite]['path']
    mytime = siteresults[hash][mysite]['time']

    sitesummary['complete_tally'] += 1

    if (len(siteresults[hash]) == 2):
        sitesummary['common_pathnames'] += 1
    else:
        sitesummary[mysite] += 1

    if processing == 'details':
        print('{},{},{}'.format(mysite, mytime, mypath))

if processing == 'summary':
    print(yaml.dump(sitesummary, default_flow_style=False))

