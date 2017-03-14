#!/usr/bin/python
# -*- coding: utf8 -*-
"""Provides convenient wrappers around calls to the Google Drive API
"""
FOLDER_TYPE = 1
MIME_TYPE_FOLDER = 'application/vnd.google-apps.folder'
MIME_TYPES_LOOKUP = {
    'application/vnd.google-apps.folder': FOLDER_TYPE
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
                item['name'].encode('utf-8'), item['id'], item['mimeType']))

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

