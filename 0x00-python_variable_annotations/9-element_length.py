#!/usr/bin/env python3
"""This module implements a type-annotated function"""
from typing import Tuple, Iterable, List, Sequence


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """This function takes an iterable of sequences and returns a list of
    tuples, where each tuple contains a sequence from the input and its
    corresponding length."""
    return [(i, len(i)) for i in lst]
