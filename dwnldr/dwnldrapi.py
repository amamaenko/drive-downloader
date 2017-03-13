#!/usr/bin/python
# -*- coding: utf8 -*-
"""Entry point for the drive-downloader application run.
"""
import io
import googleapiclient.http

from .gapiutil import find_folders, find_children_by_id, print_items



def download_files(service, folder_names):
    """Downloads files

    Args:
    """

    all_folders = []
    for folder_name in folder_names:
        res = find_folders(service, folder_name, page_size=1000)
        all_folders = all_folders + res.get('files', [])

    print_items(all_folders)

    all_files = []
    for folder in all_folders:
        res = find_children_by_id(
            service, folder['id'], page_size=1000)
        all_files = all_files + res.get('files', [])

    print_items(all_files)

    print()
    file_id = all_files[0]['id']
    file_name = all_files[0]['name']
    file_mime = all_files[0]['mimeType']
    print("Start Downloading {0}".format(file_name))
    # request = service.files().get_media(fileId=file_id)
    #request = service.files().export_media(fileId=file_id, mimeType=file_mime)
    request = service.files().export_media(fileId=file_id, mimeType='text/csv') 
    with io.open(file_name, 'wb') as fh:
        downloader = googleapiclient.http.MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

    print("Finish Downloading...")
