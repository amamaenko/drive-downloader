#!/usr/bin/python
# -*- coding: utf8 -*-
"""This module provides utility functions to deal with file names provided
through the CLI interface: clean them of quotes, split into individual files,
strip from extra spaces, etc.
"""

def str_to_tokens(user_str):
    """Split the given string into elements using the rules of separation.

    In our case the rule is simple, each token is separated by a comma (,)
    character.

    "Hello World, Yes, sir!" - will be transofrmed into:
    ["Hello World", "Yes", "sir!"]
    """
    return user_str.split(',')


def token_to_foldername(token):
    """Cleans up a given token from quotes, strip from spaces, etc.

    Args:
        token(str): 'dirty' folder name obained from the user through CLI

    Returns:
        valid folder name
    """
    foldername = token
    foldername = foldername.replace('"', '')
    foldername = foldername.strip(' ')
    return foldername


def str_to_foldernames(user_str):
    """Transform the string that 'supposedly' contains the list of folders to
    search into actual list of folder names

    Args:
        user_str(str): string obtained from the CLI interface

    Return:
        list of folder names
    """
    tokens = str_to_tokens(user_str)
    foldernames = []
    for token in tokens:
        foldernames.append(token_to_foldername(token))

    return foldernames
