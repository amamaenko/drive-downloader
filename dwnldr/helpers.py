#!/usr/bin/python
# -*- coding: utf8 -*-
'''This module contains the helper functions required for interacting with
Google Drive API
'''


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
        name contains '{0}'
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
