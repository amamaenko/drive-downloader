#!/usr/bin/python
# -*- coding: utf8 -*-
"""Entry point for the drive-downloader application run.
"""
from __future__ import print_function
import argparse
import httplib2

from oauth2client import tools
from apiclient import discovery

import gapiutil
import pathutil


HLP_DESC = """
Bulk download and convert files from a Google Drive folder to the local drive.
"""


def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 20 files.
    """
    myparser = argparse.ArgumentParser(
        parents=[tools.argparser],
        description=HLP_DESC)
    myparser.add_argument(
        "-f", "--folders",
        dest="src_folders",
        help="Specify the list of folders whose content should be downloaded")
    myparser.add_argument(
        "-d", "--dest",
        dest="dest_dir", action="store",
        default="./",
        help="Destination directory for downloaded files")

    flags = myparser.parse_args()

    credentials = gapiutil.get_credentials(flags)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    # res = get_folders(service)
    '''
    print("--")
    print(flags.src_folders)
    foldernames = pathutil.str_to_foldernames(flags.src_folders)
    items = []
    for foldername in foldernames:
        print("=== Searching for {0}".format(foldername))
        res = gapiutil.find_folders(service, foldername)
        items = res.get('files', [])
        gapiutil.print_items(items)
    '''

    res = gapiutil.find_children_by_id(service, '0B31QrTlrRsxATFN0MEtyRHRvR0k')
    items = res.get('files', [])
    gapiutil.print_items(items)

    '''
    request = service.files().list(
        pageSize=20, fields="nextPageToken, files(id, name)"
    )
    results = request.execute()
    items = results.get('files', [])
    '''

if __name__ == '__main__':
    main()
