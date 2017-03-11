#!/usr/bin/python
# -*- coding: utf8 -*-
"""Entry point for the drive-downloader application run.
"""
import httplib2

from apiclient import discovery
from .gapiutil import get_credentials, find_children_by_id, print_items

def create_service(flags):
    """Insntiates a Google Drive API service from the input parameters
    provided via CLI interface (flags)

    Args:
        flags(Object): object containing the argument strings as attributes
        of the namespace.

    Returns:
        A Resource object with methods for interacting with the service.
    """
    credentials = get_credentials(flags)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    return service


def download_files(service):
    """Downloads files

    Args:
    """

    res = find_children_by_id(
        service, '0B31QrTlrRsxATFN0MEtyRHRvR0k', page_size=1000)
    items = res.get('files', [])
    print_items(items)
