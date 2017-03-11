#!/usr/bin/python
# -*- coding: utf8 -*-
"""Entry point for the drive-downloader application run.
"""
import httplib2

from apiclient import discovery
from .gapiutil import get_credentials, find_children_by_id, print_items

def download_files(flags):
    """Downloads files

    Args:
        flags(dict): dictionary of parsed command-line parameters
    """
    credentials = get_credentials(flags)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    res = find_children_by_id(
        service, '0B31QrTlrRsxATFN0MEtyRHRvR0k', page_size=1000)
    items = res.get('files', [])
    print_items(items)
