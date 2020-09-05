#!/usr/bin/env python3
"""
This is a quick script to process a webcache, looking for strings in html files
"""

import os
import sys
from bs4 import BeautifulSoup

SITE_DIR = sys.argv[1]

def get_meta_char(file_target):
    """
    Parse the supplied file from the webcache, and look for metadata names
    """
    with open(file_target) as file_obj:
        file_contents = file_obj.read()
    soup = BeautifulSoup(file_contents, features="lxml")
    selector = 'strong'
    quotes = soup.select(selector)
    varlist = list()
    for quote in quotes:
        varlist.append(quote.text)
    return varlist

for root, dirs, files in os.walk(SITE_DIR):
    for file in files:
        if file.endswith('.html'):
            site_name = os.path.join('https://', root, file)
            file_name = os.path.join(root, file)
            verb = file_name.rsplit('/', 1)[-1].replace('.html', '')
            verb = verb.replace('-operator', '').lower()
            variables = get_meta_char(file_name)
            metadata = list()
            if len(variables) == 0:
                metadata.append('none')
            else:
                for variable in variables:
                    if '_' in variable:
                        variable = variable.replace('.', '')
                        print('{:16},{:30},{}'.format(verb, variable, file_name))
