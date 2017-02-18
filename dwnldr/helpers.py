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
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))


def find_dir(service, dir_name):
    q = '''
        mimeType = 'application/vnd.google-apps.folder' and
        name = '{0}'
    '''.format(dir_name)
    request = service.files().list(
        q=q, pageSize=20)
    results = request.execute()
    return results


def get_folders(service):
    q = '''
        mimeType = 'application/vnd.google-apps.folder' and
        name contains 'Storage'
    '''
    request = service.files().list(
        q=q,
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
