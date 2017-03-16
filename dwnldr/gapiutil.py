#!/usr/bin/python
# -*- coding: utf8 -*-
"""Provides convenient wrappers around calls to the Google Drive API
"""
import googleapiclient.http


MIME_TYPE_FOLDER = 'application/vnd.google-apps.folder'
MIME_TYPE_SHEET = 'application/vnd.google-apps.spreadsheet'
MIME_TYPE_DOC = 'application/vnd.google-apps.document'
MIME_TYPE_DRAWING = 'application/vnd.google-apps.drawing'
MIME_TYPE_FORM = 'application/vnd.google-apps.form'

# These files will not be displayed in the find list because they cannot be
# exported into something sensible
IGNORED_MIME = [
    MIME_TYPE_FORM
]

EXPORT_MIME_TABLE = {
    MIME_TYPE_SHEET: {
        'mime':'text/csv',
        'ext':'.csv'
    },
    MIME_TYPE_DOC: {
        'mime':'text/plain',
        'ext':'.txt'
    },
    MIME_TYPE_DRAWING: {
        'mime':'image/jpeg',
        'ext':'.jpg'
    }
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
    return results.get('files', [])

def find_children_files_by_id(service, parent_id, page_size):
    """Gets the list of all *files* whose parent is the file with the given
    file_id.

    NB! that if there are folders, they are left out.
    Also, the method excludes all files with mime's in the IGNORED_MIME

    Args:
        service(googleapiclient.service): adapter for the Google Drive API
        parent_id(str): file id in the Google Drive API
        page_size(int): maximum number of returned items.

    Returns:
        list of file descriptors whose parent is the file with the given
        file_id.
    """
    query = '''
        '{0}' in parents and 
        mimeType != '{1}'
    '''.format(parent_id, MIME_TYPE_FOLDER)
    all_files = _search(service, query, page_size)
    filtered_files = list(filter(
        lambda file_item: file_item['mimeType'] not in IGNORED_MIME,
        all_files))
    return filtered_files

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


def suggested_file_name(file_item):
    """Get the suggested file name for a file item. This is based on the
    EXPORT_MIME_TABLE table that appends the extension to the file name
    if it's exported from Google Drive. If it's a simply binary to download,
    then the name remains unchanged

    Args:
        file_item(dict): google drive api file dictionary item

    Returns:
        file_name(str): suggested name of the file
    """
    file_name = file_item['name']
    file_mime = file_item['mimeType']
    if file_mime in EXPORT_MIME_TABLE:
        file_name = file_name + EXPORT_MIME_TABLE[file_mime]['ext']

    return file_name

def download_file(service, file_item, out_stream):
    """Downloads file from google drive to the given output iostream
    """
    print("Trying to download {0}".format(file_item))
    file_id = file_item['id']
    file_mime = file_item['mimeType']

    # check if the file is a registered type in gapi and must be exported
    if file_mime in EXPORT_MIME_TABLE:
        export_mime = EXPORT_MIME_TABLE[file_mime]['mime']
        request = service.files().export_media(
            fileId=file_id,
            mimeType=export_mime)
    else:
        request = service.files().get_media(fileId=file_id)

    downloader = googleapiclient.http.MediaIoBaseDownload(out_stream, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
