#!/usr/bin/env python3
"""This module implements a type-annotated function to_kv"""
from typing import Tuple, Union


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """This function takes a string k and an int OR float v as arguments
    and returns a tuple."""
    the_list = [k, v ** 2]
    return tuple(the_list)
