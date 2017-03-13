#!/usr/bin/python
# -*- coding: utf8 -*-
"""Entry point for the drive-downloader application run.
"""

from .gapiutil import find_folders, find_children_by_id, print_items



def download_files(service, folder_names):
    """Downloads files

    Args:
    """

    all_folders = []
    for folder_name in folder_names:
        matching_folder_items = find_folders(service, folder_name, page_size=1000)
        all_folders = all_folders + matching_folder_items.get('files', [])

    print(all_folders)
    '''
    print(">>>>>>>>>> All matching folders")
    print_items(all_folders)
    print(">>>>>>>>>>")

    res = find_children_by_id(
        service, '0B31QrTlrRsxATFN0MEtyRHRvR0k', page_size=1000)
    items = res.get('files', [])
    # print_items(items)
    '''