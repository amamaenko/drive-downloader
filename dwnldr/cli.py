#!/usr/bin/python
# -*- coding: utf8 -*-
"""This module provides the entry point for CLI-based user interface to the
drive-downloader application
"""
import os
import argparse
import httplib2

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient import discovery

from .dwnldrapi import download_files
from .pathutil import str_to_foldernames

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive Bulk Downloader application'

HLP_DESC = """
Bulk download and convert files from a Google Drive folder to the local drive.
"""


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


def create_service(flags):
    """Insntiates a Google Drive API service from the input parameters
    provided via CLI interface (flags)

    Args:
        flags(Object): object containing the argument strings as attributes
        of the namespace.

    Returns:
        A Resource object with methods for interacting with the service.
    """
    credentials = get_credentials(flags)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    return service


def run():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 20 files.
    """
    myparser = argparse.ArgumentParser(
        parents=[tools.argparser],
        description=HLP_DESC)
    myparser.add_argument(
        "-f", "--folders", action="store",
        default="",
        required=True,
        help="Specify the list of folders whose content should be downloaded.",
        dest="src_folders")
    myparser.add_argument(
        "-d", "--dest", action="store",
        default="./",
        help="Destination directory for downloaded files.",
        dest="dest_dir")
    myparser.add_argument(
        "--dry-run", action='store_true',
        default=False,
        help="Prepare the command but not execute it. Print parsed arguments.",
        dest="is_dry")

    flags = myparser.parse_args()


    # res = get_folders(service)
    '''
    print("--")
    print(flags.src_folders)
    foldernames = pathutil.str_to_foldernames(flags.src_folders)
    items = []
    for foldername in foldernames:
        print("=== Searching for {0}".format(foldername))
        res = gapiutil.find_folders(service, foldername)
        items = res.get('files', [])
        gapiutil.print_items(items)
    '''

    if not flags.src_folders:
        print("Invalid SRC_FOLDERS argument, must be not empty.")
        return 1

    folder_names = str_to_foldernames(flags.src_folders)
    if flags.is_dry:
        print(flags)
        print(folder_names)
        return 0
    else:
        service = create_service(flags)
        download_files(service, folder_names)
