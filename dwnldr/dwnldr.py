"""Entry point for the drive-downloader application run.
"""

from __future__ import print_function
import argparse
import httplib2

from oauth2client import tools
from apiclient import discovery

import helpers


def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 20 files.
    """
    myparser = argparse.ArgumentParser(
        #parents=[tools.argparser],
        description="my sample parser")
    myparser.add_argument(
        "-t", "--test",
        dest="mtst",
        action="store")
    myparser.add_argument("-r", "--rverbosity", action="count", default=0)

    flags = myparser.parse_args()
    print(flags.mtst)

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
