#!/usr/bin/python
# -*- coding: utf8 -*-
"""Entry point for the drive-downloader application run.
"""
import httplib2

from apiclient import discovery
import gapiutil


def download_files(flags):
    """Downloads files


    Args:
        flags(dict): dictionary of parsed command-line parameters
    """
    credentials = gapiutil.get_credentials(flags)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    res = gapiutil.find_children_by_id(
        service, '0B31QrTlrRsxATFN0MEtyRHRvR0k', page_size=1000)
    items = res.get('files', [])
    gapiutil.print_items(items)
