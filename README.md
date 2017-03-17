# Drive-Downloader
A CLI application for bulk file export from the user's Google Drive's folders.

# Key functionality
- download files from a folder
  - specify the source directory name on google drive and the output directory 
    (current directory by default)
  - specify the download format (original, csv)

# Installation and Use

There are two scenarios of installing the drive-downloader tool. For both it is
highly recommended to use virtual environments as the tool requires a specific
version of the *google-api-python-client* library, so it can potentially mess
your global python installation.

## Scenario 1: Use in other projects

If I want to use the drive-downloader as a part of build process in my projects,
**her-story** for example, then I can simply add the following line into the 
*dev_requirements.txt* file of my project:

`-e git+https://github.com/amamaenko/drivedownloader.git#egg=drive-downloader`

Then I can use the util using the following command:

`python -m dwnldr`

## Scenario 2: Continue development of the tool

Simply clone the "https://github.com/amamaenko/drivedownloader.git" repository
using something like the command below:

`git clone https://github.com/amamaenko/drivedownloader.git drive-downloader`

then install a virtual environment there:

`virtualenv venv`

and, finally, install dependencies using

`pip install -r dev_requirements.txt`

## Register with Google and obtain application key

Connecting to Google API that underlies this utility requires using the OAuth2 
protocol. There are several flows in this protocol but we are going to use the
most secure - using the explicit access token. Follow the Step 1 of the
instructions located at https://developers.google.com/drive/v3/web/quickstart/python 
to get the *client_secret.json* file, and put it at any directory. Then run

'python -m dwnldr'

now you can delete the *client_secret.json*