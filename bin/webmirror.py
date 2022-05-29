#!/usr/bin/env python3
"""
This is a simple web mirror script in python
"""

import os
import sys
from pywebcopy import save_website

TMPDIR = os.path.abspath('/var/tmp')
SITEURL = 'http://help.sumologic.com/'

if len(sys.argv) > 1:
    SITEURL = sys.argv[1]

kwargs = {'project_name': 'webmirrors'}

save_website( url=SITEURL, project_folder=TMPDIR, **kwargs )
