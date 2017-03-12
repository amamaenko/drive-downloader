#!/usr/bin/python
# -*- coding: utf8 -*-
"""Acceptance tests for the CLI interface
"""
import subprocess
import os

def test_cli_dry_run():
    """Check the simple app launch with the '--dry-run' flag set.
    """
    print()
    print("Currend working directory: {0}".format(os.getcwd()))
    args = ['python', '-m', 'dwnldr', '--dry-run', '-f', '"Storage Documents"']
    result = subprocess.run(args)
    assert result.returncode == 0
