#!/usr/bin/python
"""Tests the basic CLI interface
"""
import subprocess
import os

def test_cli():
    """Check the simple app launch
    """
    print()
    print("Currend working directory: {0}".format(os.getcwd()))
    subprocess.run(['python', '-m', 'dwnldr', '--dry-run', '-f', 'Storage Documents'])

