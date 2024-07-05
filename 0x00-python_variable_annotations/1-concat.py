#!/usr/bin/env python3
"""This module implements type-annotated function"""


def concat(str1: str, str2: str) -> str:
    """This function takes a string str1 and a string str2 as arguments
    and returns a concatenated string"""
    return "{}{}".format(str1, str2)
