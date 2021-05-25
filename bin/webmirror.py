#!/usr/bin/env python3

from pywebcopy import save_website

kwargs = {'project_name': 'webmirrors'}
save_website(
    url='http://help.sumologic.com/',
    project_folder='/var/tmp/',
    **kwargs
)
