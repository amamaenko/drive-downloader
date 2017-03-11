#!/usr/bin/python
# -*- coding: utf8 -*-
"""Setup script for drive-downloader"""

from distutils.core import setup

import dwnldr


setup(name='drive-downloader',
      version=dwnldr.__version__,
      description='CLI tool to automate fetching data from Google Drive',
      author=dwnldr.__author__,
      author_email='amamaenko@gmail.com',
      packages=['dwnldr'],
      install_requires=['google-api-python-client']
     )
