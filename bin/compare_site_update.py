#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This creates a quick comparison of URL to see what s closest match
"""

import datetime
import hashlib
import urllib
import collections
import textdistance
import requests
import xmltodict
import pprint
import time
import sys
import os


sitemap = collections.defaultdict(dict)
sitemap['en'] = 'help.sumologic.com'
sitemap['jp'] = 'help.sumologic.jp'

nowdate = datetime.datetime.today()

website = collections.defaultdict(dict)
actions = collections.Counter()
uniques = collections.defaultdict(list)

AGE_LIMIT = 30
DISTANCE_LIMIT = 10
SIZE_LIMIT = .1

for mykey, myvalue in sitemap.items():

    baseurl = 'https://' + myvalue
    sitexml = baseurl + '/' + 'sitemap.xml'
    myxml = requests.get(sitexml).text
    dstamp = datetime.datetime.now().strftime('%Y%m%d')
    mydict = xmltodict.parse(myxml)

    for url in mydict['urlset']['url']:
        urlpath = url['loc']
        lastmod = url['lastmod']
        changes = url['changefreq']
        parse_object = urllib.parse.urlparse(urlpath)
        netpath = parse_object.path
        NET_HASH = hashlib.md5(netpath.encode('utf-8')).hexdigest()
        netsite = parse_object.netloc
        urldate = datetime.datetime.strptime(lastmod, "%Y-%m-%d")
        pathage = (nowdate - urldate).days

        if mykey not in website[NET_HASH]:
            website[NET_HASH][mykey] = collections.defaultdict(dict)

        website[NET_HASH][mykey]['path'] = netpath
        website[NET_HASH][mykey]['time'] = pathage
        uniques[mykey].append(netpath)

for myhash in website:
    mysitelist = list(website[myhash].keys())
    mysitelen = len(mysitelist)
    if mysitelen == 2:
        site0 = mysitelist[0]
        time0 = website[myhash][mysitelist[0]]['time']
        path0 = website[myhash][mysitelist[0]]['path']
        site1 = mysitelist[1]
        time1 = website[myhash][mysitelist[1]]['time']
        path1 = website[myhash][mysitelist[1]]['path']
        timedelta = time1 - time0

        if timedelta < 0:
            MY_STATUS = 'SAMEPATH:JPSITE:newer'
        elif timedelta > AGE_LIMIT:
            MY_STATUS = 'SAMEPATH:JPSITE:too_old'
        else:
            MY_STATUS = 'SAMEPATH:ALLSITES:path_in_sync'
    else:
        site0 = mysitelist[0]
        time0 = website[myhash][mysitelist[0]]['time']
        path0 = website[myhash][mysitelist[0]]['path']
        MY_STATUS = 'UNIQUEPATH:' + site0.upper() + 'SITE' + ':investigate_' + site0.upper()
        for mytag in sitemap.keys():
            if mytag != site0:
                for targetpath in list(uniques[mytag]):
                    distance = textdistance.damerau_levenshtein.distance(path0, targetpath)
                    if distance < DISTANCE_LIMIT:
                       if distance / len(path0) < SIZE_LIMIT:
                           MY_STATUS = 'UNIQUEPATH:' + site0.upper() + 'SITE' + ':possible_url_fixup'
    actions[MY_STATUS] += 1

for mykey, myvalue in sorted(dict(actions).items()):
    print('{:40}\t{:10}'.format(mykey, myvalue))
