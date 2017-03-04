#!/usr/bin/python
# -*- coding: utf8 -*-
'''This module contains the helper functions required for interacting with
Google Drive API
'''
import os

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive Bulk Downloader application'


def print_items(items):
    """Formatted print of the items returned by the
    Google Drive API methods
    """
    if not items:
        print("No files found.")
    else:
        print("Total files count: {0}".format(len(items)))
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))

def _search(service, query):
    """Performs a search query on Google Drive using the given 'query'

    Args:
        service(googleapiclient.service): adapter for the Google Drive API
        query(str): search query string based on the API documentation
            https://developers.google.com/drive/v3/web/search-parameters
    """
    request = service.files().list(
        q=query
    )
    results = request.execute()
    return results

def find_children_by_id(service, file_id):
    """Gets the list of all files whose parent is the file with the given
    file_id.

    Args:
        file_id(str): file id in the Google Drive API

    Returns:
        list of file descriptors whose parent is the file with the given
        file_id.
    """
    query = """'{0}' in parents""".format(file_id)
    return _search(service, query)


def find_all_files(foldername):
    """Gets the list of all files inside a folder with the given name
    """
    return 0


def find_folders(service, dir_name):
    """Gets the list of folders that match the specified dir_name

    Note that there can be multiple instance of folders with the same
    name, because Google Drive is not hierarchical.

    Args:
        dir_name(str): name of the folders to find.
    """
    query = '''
        mimeType = 'application/vnd.google-apps.folder' and
        name = '{0}'
    '''.format(dir_name)
    request = service.files().list(
        q=query, pageSize=20)
    results = request.execute()
    return results


def get_folders(service):
    """Test method
    """
    query = '''
        mimeType = 'application/vnd.google-apps.folder' and
        name contains 'Storage'
    '''
    request = service.files().list(
        q=query,
        pageSize=20
    )
    results = request.execute()
    return results


def get_credentials(flags):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Args:
        flags: command-line arguments parsed by the argparser

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials
