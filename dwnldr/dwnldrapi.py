#!/usr/bin/python
# -*- coding: utf8 -*-
"""Provides the application level API to the drive-downloader utility.
"""
import os
import io

from . import gapiutil
from . import pathutil


# assume that there are no more than 1000 results returned by the googleapi
MAGIC_PAGE_SIZE = 1000

def _find_matching_folders(service, folder_names):
    """Finds the folders that match the names in the list of folder_names.

    Args:
        service (googleapiclient.service): adapter for the Google Drive API)
        folder_names (list(str)): list of strings with "clean" folder names to
            search for in Google Drive

    Returns:
        matching_folders (list(dict)): list of dictionaries, each dict contains
            the meta-data about the folder in Google Drive: name, id, mime, etc.
    """
    matching_folders = []
    for folder_name in folder_names:
        res = gapiutil.find_folders(
            service, folder_name, page_size=MAGIC_PAGE_SIZE)
        matching_folders = matching_folders + res

    return matching_folders


def _list_contained_files(service, folder_items):
    """Lists all files contained in the Google Drive folders provided as an
    argument to this function.

    Args:
        service (googleapiclient.service): adapter for the Google Drive API)
        folder_items (list(dict)): the list of dictionaries containing the
            meta-data about the Google Drive folders: name, and id (at least!).

    Returns:
        file_items (list(dict)): the list of dictionaries containing the meta-
            information about all files contained in the Google Drive folders.
    """
    contained_files = []
    for folder in folder_items:
        res = gapiutil.find_children_files_by_id(
            service, folder['id'], page_size=MAGIC_PAGE_SIZE)
        contained_files = contained_files + res
    return contained_files

def download_files(service, folder_names, dest_dir):
    """Downloads files contained in the folders provided as one of this
    function's
    arguments.

    Args:
    """

    abs_path = pathutil.get_abs_dir_path(dest_dir)
    matching_folders = _find_matching_folders(service, folder_names)
    gapiutil.print_items(matching_folders)

    all_files = _list_contained_files(service, matching_folders)
    gapiutil.print_items(all_files)

    print()
    for file_item in all_files:
        file_name = gapiutil.suggested_file_name(file_item)
        file_path = os.path.join(abs_path, file_name)
        with io.open(file_path, 'wb') as output_file:
            gapiutil.download_file(service, file_item, output_file)


    print("Finish Downloading...")
