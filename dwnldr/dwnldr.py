from __future__ import print_function
import httplib2
import argparse

from oauth2client import tools
from apiclient import discovery

import helpers


def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 20 files.
    """
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

    credentials = helpers.get_credentials(flags)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    # res = get_folders(service)
    res = helpers.find_dir(service, "Storage Documents")
    items = res.get('files', [])
    helpers.print_items(items)

    '''
    request = service.files().list(
        pageSize=20, fields="nextPageToken, files(id, name)"
    )
    results = request.execute()
    items = results.get('files', [])
    '''

if __name__ == '__main__':
    main()