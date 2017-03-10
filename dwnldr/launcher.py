#!/usr/bin/python
# -*- coding: utf8 -*-
"""This module provides the entry point for CLI-based user interface to the
drive-downloader application
"""
import argparse
from oauth2client import tools

import dwnldr as dwnldr


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

    dwnldr.download_files(flags)


if __name__ == '__main__':
    main()
