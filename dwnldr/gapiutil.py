#!/usr/bin/python
# -*- coding: utf8 -*-
"""Provides convenient wrappers around calls to the Google Drive API
"""
import io
import googleapiclient.http


FOLDER_TYPE = 1
MIME_TYPE_FOLDER = 'application/vnd.google-apps.folder'
SHEET_TYPE = 2
MIME_TYPE_SHEET = 'application/vnd.google-apps.spreadsheet'
MIME_TYPES_LOOKUP = {
    MIME_TYPE_FOLDER: FOLDER_TYPE,
    MIME_TYPE_SHEET: SHEET_TYPE
}

def print_items(items):
    """Formatted print of the items returned by the
    Google Drive API methods
    """
    if not items:
        print("No files found.")
    else:
        print('Files:')
        print("Total count: {0}".format(len(items)))
        for item in items:
            print('{0} ({1}) -> {2}'.format(
                item['name'], item['id'], item['mimeType']))

def _search(service, query, page_size=20):
    """Performs a search query on Google Drive using the given 'query'

    Args:
        service(googleapiclient.service): adapter for the Google Drive API
        query(str): search query string based on the API documentation
            https://developers.google.com/drive/v3/web/search-parameters
        page_size(int): maximum number of returned items. Default is 20.
    """
    request = service.files().list(
        q=query,
        pageSize=page_size
    )
    results = request.execute()
    return results

def find_children_files_by_id(service, parent_id, page_size):
    """Gets the list of all *files* whose parent is the file with the given
    file_id.

    NB! that if there are folders, they are left out.

    Args:
        service(googleapiclient.service): adapter for the Google Drive API
        parent_id(str): file id in the Google Drive API
        page_size(int): maximum number of returned items.

    Returns:
        list of file descriptors whose parent is the file with the given
        file_id.
    """
    query = '''
        mimeType != '{0}' and    
        '{1}' in parents
    '''.format(MIME_TYPE_FOLDER, parent_id)
    return _search(service, query, page_size)


def find_all_files(folder_name):
    """Gets the list of all files inside a folder with the given name
    """
    return 0


def find_folders(service, folder_name, page_size=20):
    """Gets the list of folders that match the specified dir_name

    Note that the search is global, so there can be multiple instance of folders
    with the same name located on different hierarchy levels.

    Args:
        service(googleapiclient.service): adapter for the Google Drive API
        folder_name(str): name of the folder to find.
        page_size(int): maximum number of returned elements, default is 20
    """
    query = '''
        mimeType = '{0}' and
        name = '{1}'
    '''.format(MIME_TYPE_FOLDER, folder_name)
    return _search(service, query, page_size)

def export_google_doc(service, file_id, file_name):
    """Exports a Google Docs document into a file on local disk
    """
    request = service.files().export_media(fileId=file_id, mimeType='text/csv')
    with io.open(file_name, 'wb') as output_file:
        downloader = googleapiclient.http.MediaIoBaseDownload(
            output_file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

def download_binary(service, file_id, file_name):
    request = service.files().get_media(fileId=file_id)
    with io.open(file_name, 'wb') as output_file:
        downloader = googleapiclient.http.MediaIoBaseDownload(
            output_file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))