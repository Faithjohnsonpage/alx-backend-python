#!/usr/bin/env python3
"""This module implements type-annotated function"""
from typing import Union


def sum_mixed_list(mxd_lst: list[Union[int, float]]) -> float:
    """This function takes a list mxd_lst of integers and floats
    and returns their sum as a float."""
    return sum(mxd_lst)
